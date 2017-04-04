# consumer_key         = cKbhMGDG86wSUW9NfDYVxY47R
# consumer_secret      = 0Ua0fmJBUGkt1c0QazMyvoeXbRqbw9TuwDVrTVlkZUblbc4dRG
# access_token_key     = 1550177300-GL9dGzgQKXG2worTt7AoACLMd9btfvnU3oIe90a
# access_token_secret  = FlF03gLSwWjkAWGPevslbo3Zrp86X9o1zYbKveWngyEs3

import twitter

from inverted_index import InvertedIndex


popularHandles = []


def getTweets():
    """
    :return:
    """
    api = twitter.Api(consumer_key="cKbhMGDG86wSUW9NfDYVxY47R"
                      , consumer_secret="0Ua0fmJBUGkt1c0QazMyvoeXbRqbw9TuwDVrTVlkZUblbc4dRG"
                      , access_token_key="1550177300-GL9dGzgQKXG2worTt7AoACLMd9btfvnU3oIe90a"
                      , access_token_secret="FlF03gLSwWjkAWGPevslbo3Zrp86X9o1zYbKveWngyEs3")

    trends = api.GetTrendsWoeid(woeid=2459115)  # woeid of NYC = 2459115
    tweets = {}
    for trend in trends:
        tweets[trend.name] = api.GetSearch(term=trend.name, count=5)
    return tweets


def main():
    """
    :return:
    """
    tweets = getTweets()
    if tweets:
        invIndex = InvertedIndex(tweets)
