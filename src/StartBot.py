# StartBot.py
import os
from dotenv import load_dotenv

from NightBot import NightBot
from MyLogging import init_logger

load_dotenv('dev.env')

init_logger(os.getenv('LOG_FILENAME'))
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = NightBot(TOKEN, GUILD)
