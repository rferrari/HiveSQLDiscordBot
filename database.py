import re
from sqlalchemy import text
from langchain_community.utilities import SQLDatabase
from config import SQL_QUERIES, SKIP_TABLES

class Database:
    def __init__(self, config):
        self.connection_string = (
            f"mssql+pyodbc://{config['user']}:{config['password']}@"
            f"{config['server']}/{config['database']}"
            "?driver=ODBC+Driver+18+for+SQL+Server"
            "&TrustServerCertificate=yes"
            "&charset=utf8"
        )
        self.db = SQLDatabase.from_uri(self.connection_string)
        self.tables_list = []
        self.tables_schema = []
        self.tables_schema_full = {}  # Changed to dictionary
        self._initialize_tables()

    def _initialize_tables(self):
        """Initialize tables list and schema"""
        with self.db._engine.connect() as connection:
            # Get table names
            result = connection.execute(text(SQL_QUERIES["select_tables"]))
            rows = result.fetchall()
            for row in rows:
                if self._is_table_available(row[0]):
                    self.tables_list.append(row[0])

            # Get table schemas
            result = connection.execute(text(SQL_QUERIES["create_tables_schema"]))
            rows = result.fetchall()
            for row in rows:
                if self._is_table_available(row[0]):
                    self.tables_schema.append(row[0])

            # Get full table schemas with columns
            result = connection.execute(text(SQL_QUERIES["create_tables_schema_full"]))
            rows = result.fetchall()
            for row in rows:
                create_statement = row[0]
                # Extract table name from CREATE TABLE statement
                match = re.search(r'CREATE TABLE (\w+)', create_statement)
                if match:
                    table_name = match.group(1)
                    if self._is_table_available(table_name):
                        # Extract columns part from the CREATE TABLE statement
                        columns_match = re.search(r'\((.*?)\)', create_statement)
                        if columns_match:
                            self.tables_schema_full[table_name] = create_statement


        # Join lists with newlines for prompt usage
        self.tables_list = "\n".join(self.tables_list)
        self.tables_schema = "\n".join(self.tables_schema)

    def _is_table_available(self, table_name):
        """Check if table should be included"""
        return table_name not in SKIP_TABLES

    async def execute_query(self, query, fetch_size=100):
        try:
            with self.db._engine.connect() as connection:
                result = connection.execute(text(query))

                header = [col[0] for col in result.cursor.description]

                rows = result.fetchmany(fetch_size)
                # If no rows returned, return empty list but with headers
                if not rows:
                    return [], header
            
                header = [col[0] for col in result.cursor.description]
                return rows, header
        
        except Exception as e:
            print(f"Error: {str(e)}")
            return [], []


    def get_tables_list(self):
        """Return formatted table list for LLM prompt"""
        return self.tables_list
    
    def get_tables_schema(self):
        """Return formatted table schema with NO fields types for LLM prompt"""
        return self.tables_schema
    
    def get_tables_schema_full(self):
        """Return formatted table schema with fields types for LLM prompt"""
        return self.tables_schema_full
    