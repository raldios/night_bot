# StartBot.py
import os
from sys import argv
from dotenv import load_dotenv, dotenv_values, find_dotenv
from pathlib import Path
import logging

from NightBot import NightBot

try:
    args = dotenv_values(argv[1]).values()
    client = NightBot(*dotenv_values(argv[1]).values())
except IndexError as ie:
    logging.critical(ie)
    logging.critical('No .env file provided, please provide .env location as first argument.')
    exit()
