import logging
from configparser import ConfigParser
import os

CONFIG_FILE = "config.ini"


def getLogger(name):
    """
    :return: an instance of logger for logging messages
    """
    config = ConfigParser()
    config.read(CONFIG_FILE)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if name in config['log']:
        formatter = logging.Formatter('%(name)s - %(levelname)s: %(asctime)s-> %(message)s')

        fileHandler = logging.FileHandler(config['log'][name])
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(logging.DEBUG)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.ERROR)
        consoleHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        logger.addHandler(consoleHandler)

    return logger
