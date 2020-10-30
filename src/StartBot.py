# StartBot.py
import os
from sys import argv
from dotenv import load_dotenv

from NightBot import NightBot
from MyLogger import MyLogger

load_dotenv(str(argv[1]))

logger = MyLogger(os.getenv('LOG_FILENAME'))
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
INIT_CHANNEL_ID = os.getenv('INIT_CHANNEL_ID')
FACT_COOLDOWN = os.getenv('FACT_COOLDOWN')

client = NightBot(TOKEN, GUILD, INIT_CHANNEL_ID, FACT_COOLDOWN)
