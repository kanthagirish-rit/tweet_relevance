from .app_database import getDBInstance


def getTrends(woeid, category):
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
            "$match": {"trends.category": category}
        },
        {
            "$unwind": "$trends.tweets"
        },
        {
            "$group": {
                "_id": {
                    "trend": "$trends.trend"
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
    :param trend: Twitter trend/hashtag
    :param woeid: place id
    :return: tweets for the selected hashtag and place
        {
            "tweets": [
                tweetObject1,
                tweetObject2,
                .
            ],
            "woeid": "selected woeid"
        }
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
