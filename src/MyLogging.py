# MyLogging.py
import logging
from logging.handlers import RotatingFileHandler

MB_SCALAR = 1024 * 1024


def init_logger(log_filename):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(log_filename, mode='a', maxBytes=2 * MB_SCALAR,
                                       backupCount=1, encoding='utf-8', delay=False)

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info('Logger initialized')
