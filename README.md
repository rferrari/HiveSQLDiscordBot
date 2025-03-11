# 🚀 HiveSQL Discord Bot with AI Magic!  

Ever wished you could just **ask** a database a question instead of writing complex SQL queries? Well, that’s exactly what this project does! The **HiveSQL Discord Bot** lets you interact with a SQL database using natural language, making querying easier and more intuitive. Let’s dive into the cool stuff this bot can do!  

---

## 🔥 What This Bot Brings to the Table  

- **💬 Ask in Natural Language, Get SQL** – Just type your question, and the bot will generate the SQL query for you.
- **🖥️ Run SQL Directly** – If you’re more hands-on, you can execute queries manually.
- **📊 Explore Database Schema** – Check out available tables and their structures.
- **🧠 AI Assistance** – Stuck on an error? The bot can explain and guide you through it.
- **⚡ Built-in Rate Limits** – Keeps things smooth and prevents spam.

---

## 🏗️ Code Structure

### 🟢 1. The Discord Bot (HiveSQLBot.py)  
Handles everything on Discord, from user commands to admin controls. It also:  
✅ Supports command shortcuts  
✅ Includes a cooldown system  
✅ Manages errors and gives feedback  

### 🛢️ 2. Database Handler (database.py)  
This is where all the SQL magic happens. It takes care of:  
✅ Connecting to the database (HiveSQL, in this case)  
✅ Running queries safely  
✅ Caching table metadata for quick access  

### ⚙️ 3. Command Processing (commands.py)  
Every bot command goes through here. It handles:  
✅ Natural language to SQL conversion  
✅ Running SQL queries  
✅ Showing table info  
✅ Formatting query results  

### 🔧 4. Configuration (config.py)  
Everything is neatly organized in one place, including:  
✅ Discord bot settings  
✅ Database connection details  
✅ AI model configuration, supporting OpenAI and Groq
✅ Query limitations

---

## 🧠 AI-Powered Querying  

This bot isn’t just running SQL, it’s **thinking** (well, kind of). Thanks to **LangChain**, it can:  
💡 Convert human language into SQL queries  
🤖 Explain errors and suggest fixes  
📖 Help users understand database structures  
🔍 Check queries for complexity and safety  

---

## 🛠️ How to Use It  

Talking to the bot is super easy! Just use these commands:  
```
!aiquery - Convert plain English to SQL  
!hivesql - Execute SQL queries  
!tablelist - Show available tables  
!tableinfo - Display table schema  
!help - Get AI-powered assistance  
```  

---

## 🔐 Security & Performance  

Keeping things safe and efficient is a top priority! The bot includes:  
✅ Rate limiting (to prevent abuse)  
✅ Daily query limits  
✅ Error handling & sanitization  
✅ Secure credential management with environment variables  

---

## 🚀 What’s Next?  

This is just the beginning! Future improvements could include:  
- **Query result caching** for faster responses  
- **More AI models** to choose from  
- **Smarter query validation**  
- **Interactive query builder** for a more hands-on experience  
- **Query history & analytics**  
- **Plot Graphics** why not?!

---

This bot is an example of how **AI + SQL + Discord** can come together to create something truly useful. Whether you're a SQL pro or just starting out, it makes database interaction **way more intuitive**!  

🔗 **Check out the code on GitHub**: [GitHub Link](https://github.com/rferrari/HiveSQLDiscordBot)  

---

## Lets Build 🛠️

### Software Requirements
- Python 3.8+
- Microsoft ODBC Driver 18 for SQL Server
- Discord Account
- OpenAi or Groq API Key 

### Required Packages
- discord.py
- python-dotenv
- pypyodbc
- langchain
- table2ascii
- langchain-groq

## Setup 🚀

1. Clone the Repository
```bash
git clone https://github.com/yourusername/HiveSQLDiscordBot.git
cd HiveSQLDiscordBot
```

# Create Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

# Install Dependencies
```
pip install -r requirements.txt
```

## Let's install the ODBC driver

2. Add the Microsoft repository for Debian:
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/debian/11/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
```

3. Install the ODBC driver and tools:
```bash
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18
sudo apt-get install -y unixodbc-dev
```


4. Verify the installation:
```bash
odbcinst -j
```

Let's set up the ODBC driver configuration:

5. Create the ODBC driver configuration:

```bash
sudo bash -c 'cat > /etc/odbcinst.ini << EOL
[ODBC Driver 18 for SQL Server]
Description=Microsoft ODBC Driver 18 for SQL Server
Driver=/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.*.so.1.1
UsageCount=1
EOL'
```

6. Verify the driver is properly registered:

```bash
odbcinst -q -d
```

This should list the available ODBC drivers. If you see `[ODBC Driver 18 for SQL Server]` in the output, the driver is properly configured.

If you encounter any permission issues with the configuration files:

```bash
sudo chmod 644 /etc/odbcinst.ini
sudo chown root:root /etc/odbcinst.ini
```


## Configure Environment Variables 

7. Copy sample.env to .env and configure file with the following:

```
DISCORD_TOKEN=your_discord_bot_token
DISCORD_ADMIN_ID=your_discord_admin_id
OPENAI_API_KEY=your_open_ai_api_key

HIVESQL_SERVER=your_sql_server_address
HIVESQL_DATABASE=your_database_name
HIVESQL_USER=your_sql_username
HIVESQL_PWD=your_sql_password
```


# Usage 📝

The bot supports the following commands:

## Direct SQL Query
Use the `!hivesql` command to execute direct SQL queries:
```sql
!hivesql SELECT TOP 100 * FROM YourTable
```

## AI-Powered Query
Use the `!aiquery` command to ask questions in natural language:
```
!aiquery Show me the top 5 users that posted more this month
```

## Table Information Commands

### List All Tables
Use the `!tablelist` command to see all available tables:
```
!tablelist
```
This will display a list of all accessible tables in the database.

### View Table Schema
Use the `!tableinfo` command followed by a table name to see its structure:
```
!tableinfo TableName
```
This will show the complete schema for the specified table, including all columns and their types.

## Query Guidelines 📋
- Queries are automatically limited to 100 rows
- Use proper table and column names as shown in `!tableinfo`
- For complex queries, prefer `!hivesql` over `!aiquery`
- AI queries will automatically format and validate your request

## Examples 🎯

### Direct SQL Query
```sql
!hivesql SELECT TOP 10 author, title FROM Comments WHERE author = 'username' ORDER BY created DESC
```

### AI-Powered Query
```
!aiquery What are the latest comments from user 'username'?
```

### Table Information
```
!tableinfo Comments
```

# Security Considerations 🔒
-Queries are limited to 100 rows
-Only specific columns are queried
-Prevents full table scans
-Sanitizes input to reduce SQL injection risks

# Troubleshooting 🩺
-Ensure all environment variables are correctly set
-Verify ODBC driver installation
-Check network connectivity to SQL Server

# Contributing 🤝
-Fork the repository
-Create your feature branch
-Commit your changes
-Push to the branch
-Create a Pull Request

# Disclaimer ⚠️
This bot is provided as-is. Always be cautious when running SQL queries and ensure proper access controls.
