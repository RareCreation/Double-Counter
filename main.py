import asyncio
import sqlite3

import disnake
from disnake.ext import commands
from disnake.ext.commands import CommandSyncFlags
import os
from dotenv import load_dotenv

from config.config import TOKEN
from utils.console.logger_util import logger

load_dotenv()



intents = disnake.Intents(
    guilds=True,
    messages=True,
    members=True,
    message_content=True,
    voice_states=True
)

sync_flags = CommandSyncFlags.default()

try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

bot = commands.InteractionBot(intents=intents)


@bot.event
async def on_ready():
    logger.info(f"{bot.user} Bot has been loaded")

def load_cogs():
    for dirpath, _, filenames in os.walk("./cogs"):
        if "__pycache__" in dirpath:
            continue

        for filename in filenames:
            if filename.endswith(".py") and not filename.startswith("_"):
                cog_path = os.path.relpath(os.path.join(dirpath, filename), start=".").replace(os.sep, ".")[:-3]

                try:
                    bot.load_extension(cog_path)
                    logger.info(f"✅ {cog_path} has been loaded")
                except Exception as e:
                    logger.info(f"❌ Error in {cog_path}: {e}")


if __name__ == "__main__":
    load_cogs()
    bot.run(TOKEN)
