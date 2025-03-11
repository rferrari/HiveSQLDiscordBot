# HiveSQLDiscordBot 📊🔗

## Overview
HiveSQLDiscordBot is a powerful Discord bot that allows users to interact with HiveSQL databases directly through Discord channels. It offers two primary query modes:

- Direct SQL Querying
- AI-Powered Natural Language Querying

## Features ✨

### 1. Direct SQL Queries
- Use `!hivesql` command to run direct SQL queries
- Supports Microsoft SQL Server
- Limits results to 100 rows for performance

### 2. AI-Powered Querying
- Use `!aiquery` command to ask questions in natural language
- Leverages Groq's Llama3 model to translate natural language to SQL
- Intelligent query generation with built-in safety constraints

## Prerequisites 🛠️

### Software Requirements
- Python 3.8+
- Microsoft ODBC Driver 17 for SQL Server
- Discord Account
- Groq API Key

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

2. Add the Microsoft repository for Debian (since Kali is Debian-based):
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


5. Verify the installation:
```bash
odbcinst -j
```

Let's set up the ODBC driver configuration:

1. Create the ODBC driver configuration:

```bash
sudo bash -c 'cat > /etc/odbcinst.ini << EOL
[ODBC Driver 18 for SQL Server]
Description=Microsoft ODBC Driver 18 for SQL Server
Driver=/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.*.so.1.1
UsageCount=1
EOL'
```

3. Verify the driver is properly registered:

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

Copy sample.env to .env and configure file with the following:

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

### Commands Aliases

|||||
|-|-|-|-|
|AI Query|!aiquery|!ai|!ask|
|hive SQL|!hivesql|!sql|!query|
|Tables list|!tablelist|!tables|!tl|
|Table info|!tableinfo|!info|!ti|
|Help|!help|!h|!?|


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

# License 📄
As is

# Disclaimer ⚠️
This bot is provided as-is. Always be cautious when running SQL queries and ensure proper access controls.


# TODO
- plot graphics using panda
