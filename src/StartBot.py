# StartBot.py
import os
from dotenv import load_dotenv

from Bot import Bot
from MyLogging import init_logger

load_dotenv()

init_logger(os.getenv('LOG_FILENAME'))
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = Bot(TOKEN, GUILD, os.getenv('TIMEZONE'), os.getenv('JSON_FOLDER'))
