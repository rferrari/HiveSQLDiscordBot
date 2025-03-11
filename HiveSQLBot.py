import discord
from config import DISCORD_CONFIG, DB_CONFIG, LLM_CONFIG, DEBUG_MODE
from database import Database
from commands import CommandHandler
from collections import defaultdict
from datetime import datetime, timedelta

class HiveSQLBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.db = Database(DB_CONFIG)
        
        # Add command aliases
        self.command_aliases = {
            'aiquery': ['!aiquery', '!ai', '!ask'],
            'hivesql': ['!hivesql', '!sql', '!query'],
            'tablelist': ['!tablelist', '!tables', '!tl'],
            'tableinfo': ['!tableinfo', '!info', '!ti'],
            'help': ['!help', '!h', '!?']
        }

        # Create reverse lookup for faster command matching
        self.alias_to_command = {
            alias: cmd for cmd, aliases in self.command_aliases.items()
            for alias in aliases
        }

        # Create evaluator LLM
        self.eval_llm = self._setup_llm(
            temperature=LLM_CONFIG["eval_temp"], 
            name="Tables-Evaluator")

        # Create SQL generation LLM
        self.sql_llm = self._setup_llm(
            temperature=LLM_CONFIG["query_temp"], 
            name="SQL-Generator")
        
        # Could not make create_sql_prompt work 100%
        #self.query_evaluator = self.eval_llm
        # sql_prompt = self._create_sql_prompt()
        # self.llm_chain = create_sql_query_chain(
        #     self.sql_llm,
        #     self.db.db,
        #     prompt=sql_prompt
        # )
        
        self.command_handler = CommandHandler(self.db, self.sql_llm, self.eval_llm)
        
        # Add cooldown tracking
        self.COOLDOWN_DURATION = DISCORD_CONFIG["cool_down_duration"]
        self.MAX_DAILY_QUERIES = DISCORD_CONFIG["max_daily_queries"]

        self.cooldowns = defaultdict(lambda: datetime.now() - timedelta(seconds=self.COOLDOWN_DURATION+1))
        self.daily_queries = defaultdict(int)
        self.last_reset = datetime.now()

    async def on_ready(self):
        print(f'Ready! Logged in as {self.user}')

    async def on_message(self, message):
        if message.author.bot:
            return

        # Check and reset daily limits
        now = datetime.now()
        if (now - self.last_reset) > timedelta(days=1):
            self.daily_queries.clear()
            self.last_reset = now

        # Check rate limits
        user_id = str(message.author.id)

        if user_id not in DISCORD_CONFIG["admin_id"]:
            time_since_last = now - self.cooldowns[user_id]
        
            if time_since_last.total_seconds() < self.COOLDOWN_DURATION:
                await message.channel.send(
                    f"Please wait {self.COOLDOWN_DURATION - int(time_since_last.total_seconds())} "
                    "seconds before using another command."
                )
                return

            # Update cooldown only for non-admin users
            self.cooldowns[user_id] = now

            # Check daily limit
            if self.daily_queries[user_id] >= self.MAX_DAILY_QUERIES:
                await message.channel.send(
                    f"You've reached your daily limit of {self.MAX_DAILY_QUERIES} queries. "
                    "Please try again tomorrow."
                )
                return

        # Update cooldown and query count
        self.cooldowns[user_id] = now
        self.daily_queries[user_id] += 1

        # Process the command
        command = message.content.split()[0].lower()
        if command not in self.alias_to_command:
            return
        
        try:
            # Show typing indicator while processing
            async with message.channel.typing():
                # if message.content.startswith('!aiquery'):
                if any(alias == command for alias in self.command_aliases['aiquery']):
                    query = message.content[len(command):].strip()    # Remove the actual command used from message
                    response = await self.command_handler.handle_aiquery(query)
                    await message.channel.send(file=discord.File(response))

                elif any(alias == command for alias in self.command_aliases['hivesql']):
                    query = message.content[len(command):].strip()
                    response = await self.command_handler.handle_hivesql(query)
                    await message.channel.send(file=discord.File(response))

                elif any(alias == command for alias in self.command_aliases['tablelist']):
                    query = message.content[len(command):].strip()
                    response = await self.command_handler.handle_tablelist(query)
                    await message.channel.send(response)

                elif any(alias == command for alias in self.command_aliases['tableinfo']):
                    response = await self.command_handler.handle_tableinfo(message)
                    await message.channel.send(response)

                elif any(alias == command for alias in self.command_aliases['help']):
                    response = await self.command_handler.handle_help(message)
                    await message.channel.send(response)

        except Exception as e:
            print(f"Error: {str(e)}")
            await message.channel.send(f"An error occurred: {str(e)}")

    def _setup_llm(self, temperature, name, model=""):
        if not LLM_CONFIG["groq_api_key"] and not LLM_CONFIG["openai_api_key"]:
            raise ValueError("No API keys found. At least one of GROQ_API_KEY or OPENAI_API_KEY must be configured")

        # Initialize LLM based on available API key
        if LLM_CONFIG["groq_api_key"]:
            from langchain_groq import ChatGroq
            selected_model = model or LLM_CONFIG["groq_model"]
            llm = ChatGroq(
                model=selected_model,
                temperature=temperature,
                max_tokens=LLM_CONFIG["max_tokens"],
                api_key=LLM_CONFIG["groq_api_key"]
            )
            print(f"Groq Model: {selected_model} {temperature} for {name}")
        
        elif LLM_CONFIG["openai_api_key"]:
            from langchain_openai import ChatOpenAI
            selected_model = model or LLM_CONFIG["openai_model"]
            llm = ChatOpenAI(
                model=selected_model,
                temperature=temperature,
                max_tokens=LLM_CONFIG["max_tokens"],
                api_key=LLM_CONFIG["openai_api_key"]
            )
            print(f"OpenAI Model: {selected_model} {temperature} for {name}")
        
        return llm



if __name__ == "__main__":
    print("-"*30)
    print("HiveSQL Discord Bot")
    print("Starting up...")
    print("")
    bot = HiveSQLBot()
    bot.run(DISCORD_CONFIG["token"])