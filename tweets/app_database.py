from pymongo import MongoClient
from .util import config

CONFIG_FILE = "config.ini"
MONGO_LOCATION = "mongodb://localhost:27017"
DB_NAME = "tweet_relevance"


def getDBInstance():
    """
    :return:
    """
    client = MongoClient(MONGO_LOCATION)
    return client[DB_NAME]
