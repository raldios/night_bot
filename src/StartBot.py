# StartBot.py
import os
from sys import argv
from dotenv import load_dotenv

from NightBot import NightBot

load_dotenv(str(argv[1]))

client = NightBot(os.getenv('DISCORD_TOKEN'),
                  os.getenv('DISCORD_GUILD'),
                  os.getenv('INIT_CHANNEL_ID'),
                  os.getenv('FACT_COOLDOWN'),
                  os.getenv('ADD_COOLDOWN'),
                  os.getenv('LOG_FILENAME'))
