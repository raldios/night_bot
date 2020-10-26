# StartBot.py
import os
from sys import argv
from dotenv import load_dotenv

from NightBot import NightBot
from MyLogging import init_logger

load_dotenv(str(argv[1]))

init_logger(os.getenv('LOG_FILENAME'))
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
INIT_CHANNEL_ID = os.getenv('INIT_CHANNEL_ID')

client = NightBot(TOKEN, GUILD, INIT_CHANNEL_ID)
