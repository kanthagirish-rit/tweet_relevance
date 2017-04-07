import configparser
import json

import twitter

from inverted_index import InvertedIndex



popularHandles = []
configFile = "config.ini"
targetsFile = "targets.json"


def getTweets():
    """
    :return:
    """
    config = configparser.ConfigParser()
    config.read(configFile)
    api = twitter.Api(consumer_key=config['twitter']['consumer_key']
                      , consumer_secret=config['twitter']['consumer_secret']
                      , access_token_key=config['twitter']['access_token_key']
                      , access_token_secret=config['twitter']['access_token_secret'])

    trends = api.GetTrendsWoeid(woeid=2459115)  # woeid of NYC = 2459115
    tweets = {}
    print("Processing.", end="")
    for trend in trends:
        tweets[trend.name] = api.GetSearch(term=trend.name, count=1000)
        print(".", end="")
    print("\n\n")
    return tweets


def main():
    """
    :return:
    """
    tweets = getTweets()

    if tweets:
        invIndex = InvertedIndex(tweets)

        with open(targetsFile) as file:
            targets = json.load(file)
            filteredTweets = invIndex.getRelevantTweets(targets)

            print("The following are the filtered relevant tweets for each trending topic")
            print("______________________________________________________________________")
            for trend, tweets in filteredTweets.items():
                print(trend)
                for tweet in tweets:
                    print("User: " + tweet.user.name)
                    print("Tweet Text: " + tweet.text)
                    print("Re-tweet count: " + str(tweet.retweet_count))
                    print("Favorites: " + str(tweet.favorite_count))
                print("\n")

if __name__ == '__main__':
    main()