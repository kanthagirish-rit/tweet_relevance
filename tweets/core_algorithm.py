import configparser
import json

import twitter

from inverted_index import InvertedIndex


configFile = "config.ini"
targetsFile = "targets.json"


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
    config = configparser.ConfigParser()
    config.read(configFile)
    api = twitter.Api(consumer_key=config['twitter']['consumer_key']
                      , consumer_secret=config['twitter']['consumer_secret']
                      , access_token_key=config['twitter']['access_token_key']
                      , access_token_secret=config['twitter']['access_token_secret'])

    trends = api.GetTrendsWoeid(woeid=woeid)  # woeid of NYC = 2459115
    tweets = {}
    print("Processing.", end="")
    for trend in trends:
        tweets[trend.name] = api.GetSearch(term=trend.name, count=1000)
        print(".", end="")
    print("\n\n")
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

        with open(targetsFile) as file:
            targets = json.load(file)
            filteredTweets = invIndex.getRelevantTweets(targets)

            print("The following are the filtered relevant tweets for each trending topic")
            print("______________________________________________________________________")
            for trend, tweets in filteredTweets.items():
                if tweets:
                    print(trend)
                    for tweet in tweets:
                        print("User: " + tweet.user.name)
                        print("Tweet Text: " + tweet.text)
                        print("Re-tweet count: " + str(tweet.retweet_count))
                        print("Favorites: " + str(tweet.favorite_count))
                    print("\n")

if __name__ == '__main__':
    test()