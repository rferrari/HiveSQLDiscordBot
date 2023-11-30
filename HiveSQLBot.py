import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
import pypyodbc
from table2ascii import table2ascii as t2a, PresetStyle

load_dotenv()

discordToken = os.environ.get("DISCORD_TOKEN")
discordAdmin = os.environ.get("DISCORD_ADMIN_ID")

hivesqlServer = os.environ.get("HIVESQL_SERVER")
hivesqlDatabase = os.environ.get("HIVESQL_DATABASE")
hivesqlUser = os.environ.get("HIVESQL_USER")
hivesqlPwd = os.environ.get("HIVESQL_PWD")

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
 
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
 
    if message.content.startswith('hi'):
        await message.channel.send(message.author)

    if message.content.startswith('!hivesql'):
        params = message.content.split(" ", 1)
        SQLCommand = params[1]

        connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                        'Server='+hivesqlServer+';'
                                        'Database='+hivesqlDatabase+';'
                                        'uid='+hivesqlUser+';'
                                        'pwd='+hivesqlPwd)

        cursor = connection.cursor()
        result = cursor.execute(SQLCommand)
        result = result.fetchmany(100)
        connection.close()

        #print(result)

        header = []
        for column in cursor.description:
            header.append(column[0])

        output = t2a(
            header=header,
            body=result,
            style=PresetStyle.thin_compact
        )

        f = open("sqlresult.txt", "w")
        f.write(output)
        f.close()
        await message.channel.send(file=discord.File(r'sqlresult.txt'))
        #await message.channel.send(f"```\n{output}\n```")
        return
    

 
client.run(discordToken)