import logging
from configparser import ConfigParser

CONFIG_FILE = "config.ini"
config = ConfigParser()
config.read(CONFIG_FILE)


def getLogger(name):
    """
    :return: an instance of logger for logging messages
    """
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


def getStopwords():
    """
    :return:
    """
    stopWords = []
    stopwordsFile = config['training']['twitter_stopwords']
    with open(stopwordsFile, 'r') as file:
        stopWords.extend([line.strip().lower() for line in file
                          if len(line.strip()) > 0])
    return sorted(stopWords)
