from pymongo import MongoClient
from util import config


def getDBInstance():
    """
    :return:
    """
    client = MongoClient(config['mongodb']['database_location'])
    return client[config['mongodb']['database_name']]
