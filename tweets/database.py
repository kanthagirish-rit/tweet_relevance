from pymongo import MongoClient
import configparser

CONFIG_FILE = "config.ini"
MONGO_LOCATION = "mongodb://localhost:27017"

db = None


def getDBInstance():
    """
    :return:
    """
    if db is None:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        client = MongoClient(MONGO_LOCATION)
        global db
        db = client[config['mongodb']['database_name']]
        return db
    else:
        return db
