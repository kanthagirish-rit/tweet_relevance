from pymongo import MongoClient
from .util import config

CONFIG_FILE = "config.ini"
MONGO_LOCATION = "mongodb://localhost:27017"
DB_NAME = "tweet_relevance"
db = None


def getDBInstance():
    """
    :return:
    """
    if db is None:
        client = MongoClient(MONGO_LOCATION)
        global db
        db = client[DB_NAME]
        return db
    else:
        return db
