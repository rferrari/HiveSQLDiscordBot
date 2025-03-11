import re
import asyncio
from config import DEBUG_MODE
from table2ascii import table2ascii as t2a, PresetStyle
from langchain_core.prompts import PromptTemplate

class CommandHandler:
    def __init__(self, db, llm_chain, query_evaluator):
        self.db = db
        self.llm_chain = llm_chain
        self.query_eval = query_evaluator

    async def handle_hivesql(self, sql_query, user_display_name):
        """Handle !hivesql command - execute user query"""
        # sql_query = message.content.split(" ", 1)[1]
        try:
            rows, header = await self.db.execute_query(sql_query)
            # Check if the query returned empty results
            if not rows or not header:
                return "Query executed, but no results found. Please check your query."
            return await self._format_response(None, rows, header)
        except Exception as e:
            ai_explain = await self.handle_help(
                "Explain and/or suggest new query for this error format:\n" + str(e), user_display_name, False)
            return f"{ai_explain}\n\n```\n{str(e)}\n```"
        

    async def handle_aiquery(self, message, user_display_name):
        """Handle !aiquery command - try to create sql query from text"""
        # Use retry logic
        sql_query, rows, header = await self.retry_sql_generation(message)
        
        if sql_query:
            return await self._format_response(sql_query, rows, header)
        else:
            raise Exception("Failed to generate valid SQL query")


    async def handle_tablelist(self, message, user_display_name):
        """Handle !tablelist command - shows all available tables"""
        try:
            tables = self.db.get_tables_list()
            response = "Available Tables:\n```sql\n"
            response += tables
            response += "\n```"
            return response
        except Exception as e:
            if (DEBUG_MODE):
                print(f"Error in !tablelist: {str(e)}")
            return (f"An error occurred: {str(e)}")


    async def handle_tableinfo(self, message, user_display_name):
        """Handle !tableinfo table_name - shows schema for specific table"""
        try:
            # Split message and get second word
            params = message.split()
            if len(params) < 2:
                return "Please specify a table name. Usage: !tableinfo <tablename>"
            
            table_name = params[1].lower()  # Get second word and convert to lowercase
            
            # Search for matching table schema in database schemas
            matching_schemas = [schema for schema in self.db.get_tables_schema().split('\n')
                              if table_name in schema.lower()]
            
            if matching_schemas:
                response = "Table Schema:\n```sql\n"
                response += "\n".join(matching_schemas)
                response += "\n```"
                return response
            else:
                return (f"No table schema found for '{table_name}'")
                
        except Exception as e:
            if (DEBUG_MODE):
                print(f"Error in !tableinfo: {str(e)}")
            return (f"An error occurred: {str(e)}")


    async def handle_help(self, help_text, user_display_name, include_tables=True):
        """Handle !help command - provides conversational help about tables and queries"""
        try:
            # Create help context with available information
            help_context = self._create_help_prompt()

            if (include_tables):
                tables_list = self.db.get_tables_list()
            else:
                tables_list = ""

            formatted_prompt = help_context.format(
                        help_text=help_text,
                        tables_list=tables_list,
                        username=user_display_name,
                        dialect="mssql"
                    )
            if (DEBUG_MODE):
                print("Formatted Prompt:", formatted_prompt)

            # Get response from LLM
            help_response = self.llm_chain.invoke(formatted_prompt)

            return help_response.content
                               
        except Exception as e:
            print(f"Error in !help: {str(e)}")
            return (f"An error occurred: {str(e)}")

    async def _format_response(self, sql_query, rows, header):
        """Format response data to readable table format"""
        output = t2a(
            header=header,
            body=rows,
            style=PresetStyle.thin_compact
        )
        
        with open("sqlresult.txt", "w", encoding='utf-8') as f:
            if sql_query:  # Only include query if it exists
                f.write(f"Query: {sql_query}\n\nResults:\n{output}")
            else:
                f.write(str(output))
        return "sqlresult.txt"
    
    def extract_JsonContent(self, text):
        # Extract SQL query block from different models response
        match = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Try to extract from generic Markdown code blocks
        match = re.search(r'```\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Try to extract the first code block, ignoring any text after it
        match = re.search(r'```(.*?)```', text, re.DOTALL)
        if match:
            # Extract content between first ``` and next ```
            inner_text = match.group(1)
            # Remove any language identifier if present
            inner_text = re.sub(r'^[a-zA-Z]+\n', '', inner_text)
            return inner_text.strip()

        # If no Markdown blocks found, clean and return the text
        return text.strip()

    def extract_sql(self, text):
        # Try to extract SQL inside Markdown code blocks with language
        match = re.search(r'```sql\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Try to extract from generic Markdown code blocks
        match = re.search(r'```\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Try to extract the first code block, ignoring any text after it
        match = re.search(r'```(.*?)```', text, re.DOTALL)
        if match:
            # Extract content between first ``` and next ```
            inner_text = match.group(1)
            # Remove any language identifier if present
            inner_text = re.sub(r'^[a-zA-Z]+\n', '', inner_text)
            return inner_text.strip()

        # If no Markdown blocks found, clean and return the text
        text = re.sub(r'\\(.)', r'\1', text)  # Remove escape characters
        return text.strip()
    

    async def retry_sql_generation(self, query_text, max_retries=3, retry_delay=2):
        """Attempt to execute Ai Query Max_Retries, if fail, ask ai to rebuild search query"""
        last_error = None
        
        # get relevants tables based on user input
        evaluator_prompt = self._create_evaluator_prompt(query_text)
        formatted_prompt = evaluator_prompt.format(
                        input=query_text,
                        tables_list=self.db.get_tables_list()
                    )
        if (DEBUG_MODE):
            print("Formatted Prompt:", formatted_prompt)

        llm_response = self.llm_chain.invoke(formatted_prompt)
        if (DEBUG_MODE):
            print(f"Raw evaluator response: {llm_response.content}")

        # Extract table names from response more safely
        table_list_str = self.extract_JsonContent(llm_response.content)
        # Remove brackets and clean up whitespace
        table_list_str = table_list_str.replace('[', '').replace(']', '').strip()
        # Split by comma and clean each table name
        suggested_tables = [
            table.strip().strip('"\'[]') 
            for table in table_list_str.split(',')
            if table.strip()
        ]
        if (DEBUG_MODE):
            print(f"Suggested tables: {suggested_tables}")

        # Get full schema for suggested tables
        relevant_schemas = {}
        for table in suggested_tables:
            try:
                schema = self.db.get_tables_schema_full().get(table)
                if schema:
                    relevant_schemas[table] = schema
                    if (DEBUG_MODE):
                        print(f"Found schema for table: {table}")
            except KeyError as e:
                print(f"Warning: Table {table} not found in schema")
                continue
        
        if not relevant_schemas:
            raise Exception(f"No valid tables found among suggestions: {suggested_tables}")
        
        if (DEBUG_MODE):
            print(f"Relevant schemas: {relevant_schemas}")

        # Format relevant schemas for the LLM
        schemas_info = "\n".join([
            f"{schema}"
            for table, schema in relevant_schemas.items()
        ])
        if (DEBUG_MODE):
            print(f"Schemas being used:\n{schemas_info}")

        for attempt in range(max_retries):
            try:
                # Get raw response from LLM
                #if (DEBUG_MODE):
                    #print(self.llm_chain)

                try:
                    sql_prompt = self._create_sql_prompt()
                    formatted_prompt = sql_prompt.format(
                        input=query_text,
                        dialect="mssql",
                        top_k=100,
                        table_info=schemas_info
                    )
                    # if (DEBUG_MODE):
                    #     print("Formatted Prompt:", formatted_prompt)
                    
                    # chain = RunnablePassthrough() | self.llm_chain
                    llm_response = self.llm_chain.invoke(formatted_prompt)
                except Exception as e:
                    print(f"Error accessing prompt: {e}")

                # langchain sql chain not working 100%
                # llm_response = self.llm_chain.invoke({
                #     "question": "",
                #     "input": query_text,
                #     "table_info": schemas_info,
                #     "dialect": "mssql",
                #     "top_k": "100"
                # },config={"verbose": True})
                
                # Extract SQL from LLM response
                sql_query = self.extract_sql(llm_response.content)
                print("--"*30)
                print(f"Attempt {attempt + 1} - Generated SQL:\n{sql_query}")
                print("")
                
                # Test the query execution
                rows, header = await self.db.execute_query(sql_query)
                return sql_query, rows, header

            except Exception as e:
                last_error = str(e)
                error_context = f"""
Attempt failed with error: {last_error}
Please fix the SQL query considering the error message and tables schema.
Try Other Table or Fix Colluns names exactly how is described on schema.
"""
                # Add error context to next attempt
                query_text = f"{query_text}\n\n{error_context}"
                print("=="*30)
                print(f"ERROR: ATTEMPT {attempt + 1} FAILED:\n{last_error}")
                print("")
                
                if attempt == max_retries - 1:
                    raise Exception(f"Failed after {max_retries} attempts. Last error: {last_error}")
                
                # Wait briefly before retry
                await asyncio.sleep(retry_delay)

        return None, None, None
    

    def _create_sql_prompt(self):
        """
        Create a custom SQL query prompt template for SQL query generation.
        Args: top_k (int, optional): Default number of rows to limit in queries. Defaults to 5.
        Returns: PromptTemplate: A prompt template for SQL query generation
        """
        # Define the SQL prompt template
        SQL_PROMPT = """
You are a {dialect} expert. Given an input question, create a syntactically correct T-SQL query to run.

# Key T-SQL Guidelines:
- IMPORTANT: DO NOT create DELETE, UPDATE, INSERT sql statements
- If user asks for specific number (e.g., "last post", "last 5 posts"), use that number after TOP
- If no number specified, default to TOP {top_k}
- Query columns necessary to answer the specific question.
- Always place TOP N immediately after SELECT: 'SELECT TOP N column1, column2'
- Always Use square brackets [] for table and column names
- Use table and columns name as specified in the Schema
- Pay attention to use only Tables and column names you can see in the Schema.

# Query Constraints:
- Ignore ID collum, just used for internal database usage
- Accounts username is on [name] column
- Finding posts: Use Comments table with title <> ''
- Finding comments: Use Comments table with title = ''
- Tracking transfers: Use TxTransfers table (maybe users request transactions intead transfers)
- Blockchain data: Use Transactions table
- Treasury/funding: Use VODHFFundings table

# Tables Schema:
{table_info}

Question: {input}

RESPOND ONLY THE SQL Query:
"""

        return PromptTemplate(
            input_variables=['input', 'top_k', 'dialect', 'table_info'],
            template=SQL_PROMPT,
        )
    

    def _create_evaluator_prompt(self, input):
        """
        Create a custom SQL query prompt template for SQL query generation.
        Args: top_k (int, optional): Default number of rows to limit in queries. Defaults to 5.
        Returns: PromptTemplate: A prompt template for SQL query generation
        """
        TABLE_SELECTION_PROMPT = """
You are an expert mssql T-SQL database analyst tasked with selecting the most relevant tables to answer a specific user query.

# Task Guidelines:
- Carefully analyze the user's question and the available tables
- Select ONLY tables that are directly relevant to answering the query
- Consider table relationships, foreign keys, and potential joins
- Be comprehensive but precise in table selection
- Avoid including unnecessary tables that won't contribute to the query

# Evaluation Criteria:
1. Direct data relevance
2. Potential for meaningful joins
3. Columns that match query requirements
4. Minimal but sufficient table set

# User Question: {input}

# Response Requirements:
- Respond ONLY with a JSON-formatted list of table names
- If no tables are relevant, return an empty list: []

# Important Notes:
- Be strategic and think through table relationships
- Consider implicit connections between tables
- Quality of table selection is crucial for query accuracy
- RAW Output No explanations

# OUTPUT JUST FORMAT:
```json
["Customers", "Orders", "Products"]
```

# Available Tables:
{tables_list}
"""

        # Prompt Template
        return PromptTemplate(
            input_variables=['input', 'tables_list'],
            template=TABLE_SELECTION_PROMPT
        )
    
    def _create_help_prompt(self):
        HELP_PROMPT = """
You are a helpful {dialect} T-SQL assistant. Help {username} understand how to query the Hive blockchain data.

{username} Question: {help_text}

Provide a helpful response with examples if applicable in Discord Markdown text.

# Queries Helper
- Always place TOP N immediately after SELECT: 'SELECT TOP N column1, column2'
- Always Use square brackets [] for table and column names

# Available Commands:
- !aiquery: Generate SQL queries from natural language
- !hivesql: Execute direct SQL queries
- !tablelist: Show all available tables
- !tableinfo: Show specific table schema
- !help: Ask question so I can help

# Available Tables and Their Purpose:
{tables_list}

# Command Aliases
'aiquery': ['!aiquery', '!ai', '!ask'],
'hivesql': ['!hivesql', '!sql', '!query'],
'tablelist': ['!tablelist', '!tables', '!tl'],
'tableinfo': ['!tableinfo', '!info', '!ti'],
'help': ['!help', '!h', '!?']
"""
        return PromptTemplate(
            input_variables=['tables_list', 'help_text', 'dialect', 'username'],
            template=HELP_PROMPT
        )