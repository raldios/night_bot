# StartBot.py
import os
from sys import argv
from dotenv import load_dotenv
from pathlib import Path

from NightBot import NightBot

env_path = Path(str(argv[1]))
if not env_path.exists():
    print('CRITICAL - ENV FILE NOT FOUND, EXITING')
    exit()

load_dotenv(env_path)

client = NightBot(os.getenv('DISCORD_TOKEN'),
                  os.getenv('DISCORD_GUILD'),
                  os.getenv('INIT_CHANNEL_ID'),
                  os.getenv('FACT_COOLDOWN'),
                  os.getenv('LOG_FILENAME'))
