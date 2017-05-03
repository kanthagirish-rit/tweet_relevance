from .database import getDBInstance


def getTrends(woeid):
    """
    :param woeid: a unique integer representation of the place
    :return: a python list of python dictionaries of the following structure
        data = [{
            "trend" : "name",
            "count" : #_of_tweets,
            "category" : "category to which the trend belongs"
        }]
    """
    db = getDBInstance()
    payload = [
        {
            "$match": {"woeid": woeid}
        },
        {
            "$unwind": "$trends"
        },
        {
            "$unwind": "$trends.tweets"
        },
        {
            "$group": {
                "_id": {
                    "trend": "$trends.trend",
                    "category": "$trends.category"
                },
                "count": {"$sum": 1}
            }
        }
    ]
    cursor = db.trends.aggregate(payload)
    data = []
    for document in cursor:
        data.append(document)
    return data


def getTweets(trend, woeid):
    """
    :param trend:
    :return:
    """
    db = getDBInstance()
    payload = [{
                "$match": {"woeid": woeid}
            },
            {
                "$unwind": "$trends"
            },
            {
                "$match": {"trends.trend": trend}
            },
            {
                "$group": {
                    "_id": "$trends.tweets"
                }
            }]
    result = db.trends.aggregate(payload).next()
    data = {
        "tweets": result["_id"],
        "woeid": woeid
    }
    return data
