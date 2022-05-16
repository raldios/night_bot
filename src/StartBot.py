# StartBot.py
from sys import argv
from dotenv import dotenv_values
import logging

from NightBot import NightBot

try:
    startup_dict = dotenv_values(argv[1])
    client = NightBot(startup_dict)
except IndexError as ie:
    logging.critical(ie)
    logging.critical('No .env file provided, please provide .env location as first argument.')
    exit()
