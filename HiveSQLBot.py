import discord
import asyncio
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
        super().__init__(
            command_prefix='!', 
            intents=intents,
            reconnect=True,             # Enable auto-reconnect
            heartbeat_timeout=60.0,     # Increase heartbeat timeout
            guild_ready_timeout=5.0     # Reduce guild timeout
        )
        
        # Create event loop for async operations    
        self.loop = asyncio.get_event_loop()

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
        print(f'Logged in Discord as {self.user}')
        print(f'Ready!')

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
        user_display_name = message.author.display_name

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
                    response = await self.execute_with_timeout(
                        await self.command_handler.handle_aiquery(query, user_display_name),
                        timeout=120  # 5 minutes max
                    )

                    await message.channel.send(
                        content=f"{user_display_name}, here is your query results:", 
                        file=discord.File(response))

                elif any(alias == command for alias in self.command_aliases['hivesql']):
                    query = message.content[len(command):].strip()
                    response = await self.command_handler.handle_hivesql(query, user_display_name)
                    if (response == "sqlresult.txt"):
                        await message.channel.send(
                            content=f"{user_display_name}, here is your query results:", 
                            file=discord.File(response))
                    else:
                        await message.channel.send(response)

                elif any(alias == command for alias in self.command_aliases['tablelist']):
                    query = message.content[len(command):].strip()
                    response = await self.command_handler.handle_tablelist(query, user_display_name)
                    await message.channel.send(response)

                elif any(alias == command for alias in self.command_aliases['tableinfo']):
                    response = await self.command_handler.handle_tableinfo(message.content, user_display_name)
                    await message.channel.send(response)

                elif any(alias == command for alias in self.command_aliases['help']):
                    response = await self.command_handler.handle_help(message.content, user_display_name)
                    await message.channel.send(response)

        except TimeoutError:
            await message.channel.send("Query took too long to execute. Please try a simpler query.")
        except Exception as e:
            print(f"Error: {str(e)}")
            await message.channel.send(f"An error occurred: {str(e)}")


    async def on_disconnect(self):
            """Handle disconnection events"""
            if DEBUG_MODE:
                print("Bot disconnected from Discord. Attempting to reconnect...")
            
            # Attempt to reconnect
            retry_count = 0
            while not self.is_closed() and retry_count < 5:
                try:
                    await self.start(DISCORD_CONFIG["token"])
                    break
                except Exception as e:
                    retry_count += 1
                    if DEBUG_MODE:
                        print(f"Reconnection attempt {retry_count} failed: {e}")
                    await asyncio.sleep(5 * retry_count)  # Exponential backoff

    async def execute_with_timeout(self, coroutine, timeout=60):
        """Execute a coroutine with timeout in a separate task"""
        try:
            # Create task to run in background
            task = asyncio.create_task(coroutine)
            return await asyncio.wait_for(task, timeout=timeout)
        except asyncio.TimeoutError:
            # Cancel the task if it times out
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            raise TimeoutError("Query execution took too long")

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
    while True:
        try:
            bot = HiveSQLBot()
            bot.run(DISCORD_CONFIG["token"])
        except Exception as e:
            if DEBUG_MODE:
                print(f"Bot crashed: {e}")
            print("Restarting bot in 5 seconds...")
            asyncio.sleep(5)