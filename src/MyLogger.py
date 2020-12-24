# MyLog.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from discord import TextChannel

MB_SCALAR = 1024 * 1024


class MyLogger:

    def __init__(self, log_filename, bot):
        self.bot = bot

        self.init_logger(log_filename)

    @staticmethod
    def init_logger(log_filename):
        cwd = Path.cwd()
        log_location = cwd.parent / log_filename

        logging.getLogger('discord').setLevel(logging.WARNING)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = RotatingFileHandler(log_location, mode='a', maxBytes=2 * MB_SCALAR,
                                           backupCount=0, encoding='utf-8', delay=False)

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.info('Logger initialized')

    @staticmethod
    async def debug(message: str):
        logging.debug(message)

    async def info(self, message: str):
        log_channel: TextChannel = self.bot.get_log_channel()

        logging.info(message)
        await log_channel.send(message)

    async def warning(self, message: str):
        log_channel: TextChannel = self.bot.get_log_channel()

        logging.warning(message)
        await log_channel.send(message + '<@82331305387241472>')

    async def error(self, message: str):
        log_channel: TextChannel = self.bot.get_log_channel()

        logging.error(message)
        await log_channel.send(message + '<@82331305387241472>')

    async def critical(self, message: str):
        log_channel: TextChannel = self.bot.get_log_channel()

        logging.critical(message)
        await log_channel.send(message + '<@82331305387241472>')
