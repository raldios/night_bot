# StartBot.py
import os
from sys import argv
from dotenv import load_dotenv
from pathlib import Path

from NightBot import NightBot

if len(argv) < 2:
    print('CRITICAL - ENV FILE NOT PROVIDED, EXITING')
    exit()

env_path = Path(str(argv[1]))
if not env_path.exists():
    print('CRITICAL - ENV FILE DOES NOT EXIST, EXITING')
    exit()

load_dotenv(env_path)

client = NightBot(os.getenv('DISCORD_TOKEN'),
                  os.getenv('DISCORD_GUILD'),
                  os.getenv('INIT_CHANNEL_ID'),
                  os.getenv('FACT_COOLDOWN'),
                  os.getenv('LOG_FILENAME'))
