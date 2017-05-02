"""
python version:3.5
"""

__author__ = "Kantha Girish", "Pankaj Uchil Vasant", "Samana Katti"

import json

import twitter

from inverted_index import InvertedIndex
from database import getDBInstance
from util import getLogger, config


TARGETS_FILE = "targets.json"
logger = getLogger("populate_feed")


def getTweets(woeid):
    """
    :param woeid : Where On Earth ID of the place of interest for which trends and related
        tweets are to be extracted.
    :return: A python dictionary containing keys as trends and the values as the list of tweets
        fetched from the twitter API call.
        tweets = {
                    "trend1": [tweet1, tweet2, ...],
                    "trend2": [tweet3, tweet4, ...]
                }

    This function reads config file `config.ini` containing the access keys for twitter API
    calls and creates a connection to the twitter API. The trends are fetched for the
    specified `woeid` and the tweets are fetched for each trend. The result is returned as a
    python dictionary
    """
    api = twitter.Api(consumer_key=config['twitter']['consumer_key']
                      , consumer_secret=config['twitter']['consumer_secret']
                      , access_token_key=config['twitter']['access_token_key']
                      , access_token_secret=config['twitter']['access_token_secret'])

    trends = api.GetTrendsWoeid(woeid=woeid)  # woeid of NYC = 2459115
    tweets = {}
    logger.debug("getTweets(): fetching trends")
    for trend in trends:
        tweets[trend.name] = api.GetSearch(term=trend.name
                                           , count=config['twitter']['fetch_count'])
        
    return tweets


def test():
    """
    :return: None

    This function runs the test case to fetch tweets for NYC and filter them according to
    the list of popular/celebrity twitter handles manually created. The final result is
    tweets by the popular/celebrity twitter handles for the trending topics. This is printed
    on the console.
    """
    woeid = 2459115         # NYC
    tweets = getTweets(woeid)

    if tweets:
        invIndex = InvertedIndex(tweets)

        with open(TARGETS_FILE) as file:
            targets = json.load(file)
            filteredTweets = invIndex.getRelevantTweets(targets['targets'])

            print("The following are the filtered relevant tweets for each trending topic\n\n")
            tweetCount = 0
            for trend, tweets in filteredTweets.items():
                if tweets:
                    print("Trend: " + trend)
                    print("__________________________________________________________________")

                    tweetCount += len(tweets)
                    for tweet in tweets:
                        print("User: " + tweet.user.name)
                        print("Tweet Text: " + tweet.text)
                        print("Re-tweet count: " + str(tweet.retweet_count))
                        print("Favorites: " + str(tweet.favorite_count) + "\n")
                    print("\n")
            if tweetCount == 0:
                print("Looks like no one (in our list) has tweeted on current trends!")


def main():
    """
    :return: None

    This is method is executed when this file is run as a python script
    """
    db = getDBInstance()
    cursor = db.places.find({})

    logger.debug("main(): Beginning to fetch tweets and create Inverted Index")
    woeids = [2459115, 2442047, 2490383]
    for document in cursor:
        woeid = int(document['woeid'])
        logger.debug("main(): Working on woeid-{}".format(woeid))
        tweets = getTweets(woeid)
        if tweets:
            invIndex = InvertedIndex(tweets)

            logger.debug("main(): calling writeToDB()")
            invIndex.writeToDB(woeid)
            del invIndex

if __name__ == '__main__':
    main()
