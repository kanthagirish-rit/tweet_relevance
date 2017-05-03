"""
python version:3.5
"""

__author__ = "Kantha Girish", "Pankaj Uchil Vasant", "Samana Katti"

import json
import datetime

from database import getDBInstance
import util
from naivebayes import NaiveBayes


class InvertedIndex:
    """
    This class implements the inverted index logic to create inverted index on trending
    topics and tweets. In this case, the documents are the trends themselves and the
    termList will be Twitter handles(Twitter usernames). An entry of python-twitter's
    `Status` object, which is the Tweet, is added to the postings list against each trend
    for each user, if he has tweeted under the trend.
    """
    __slots__ = ["twitterHandles", "trends", "indexLists", "logger", "totalTweets",
                 "categories"]

    def __init__(self, tweets):
        self.twitterHandles = []
        self.trends = []
        self.categories = []
        self.indexLists = []
        self.logger = util.getLogger("populate_feed.InvertedIndex")
        self.totalTweets = 0

        self._populate(tweets)

    def _populate(self, tweets):
        """
        :param tweets: A python dictionary containing trends as keys and list of tweets as
        values against each trend.
        :return: None

        This is a private method used by the constructor to populate the inverted index object
        """
        for trendName in tweets:
            self.trends.append(trendName)
            self.totalTweets += len(tweets[trendName])

            # classify trend
            tweetsDoc = " ".join([tweet.text for tweet in tweets[trendName]])
            model = NaiveBayes()
            model.loadModelFromDB()
            self.categories.append(model.classify(tweetsDoc))

            for tweet in tweets[trendName]:
                if tweet.user.screen_name not in self.twitterHandles:
                    self.twitterHandles.append(tweet.user.screen_name)
                    posts = [(self.trends.index(trendName), tweet)]
                    self.indexLists.append(posts)
                else:
                    posts = self.indexLists[self.twitterHandles.index(tweet.user.screen_name)]
                    posts.append((self.trends.index(trendName), tweet))
        self.logger.debug('Created and populated Inverted Index: Trends-{}, Tweets-{}'.format(
            len(self.trends), self.totalTweets))

    def search(self, handle):
        """
        :param handle: the twitter handle  for which the search is to be performed
        :return: the list of tweets for the given twitter handle if exist, else an empty list.

        This method returns the list of tweets for the given twitter handle if the handle exits
        in the list of known twitter handles.
        """
        if handle in self.twitterHandles:
            return self.indexLists[self.twitterHandles.index(handle)]
        else:
            return []

    def getRelevantTweets(self, targetHandles):
        """
        :param targetHandles: A python list of target twitter handles of popular
        people/celebs with the keys as twitter handles.
        :return: A python dictionary of keys as the trends and the values as list of tweets
        filtered by the list of target twitter handles.
                tweets = {
                    "trend1": [tweet1, tweet2, ...],
                    "trend2": [tweet3, tweet4, ...]
                }

        This method takes a dictionary of target twitter handles and returns the tweets of
        those handles segregated into trends as a python dictionary.
        """
        tweets = {}
        for trend in self.trends:
            tweets[trend] = []
        for target in targetHandles:
            posts = self.search(target)
            if posts:
                for trendIndex, post in posts:
                    tweets[self.trends[trendIndex]].append(post)
        return tweets

    def writeToDB(self, woeid):
        """
        :param woeid: unique id of the place for which the trends and corresponding tweets
            were fetched.
        :return: None

        This method writes the filtered tweets to the database for the given woeid.
        """
        db = getDBInstance()
        self.logger.debug('writeToDB() before writing')

        targetDocument = db.targets.find_one({})
        targets = targetDocument['targets']

        trendingData = {
            trend: [] for trend in self.trends
        }

        filteredCount = 0
        for target in targets:
            posts = self.search(target)
            if posts:
                filteredCount += len(posts)
                for trendIndex, post in posts:
                    trendingData[self.trends[trendIndex]].append(json.loads(str(post)))

        data = []
        for trend in trendingData:
            d = {
                "trend": trend,
                "tweets": trendingData[trend],
                "category": self.categories[self.trends.index(trend)]
            }
            data.append(d)

        if filteredCount > 0:
            db.trends.update_one({
                    "woeid": woeid
                },
                update={
                    "$set": {
                        "trends": data,
                        "updated": datetime.datetime.now()
                    }
                },
                upsert=True
            )

            self.logger.debug('writeToDB(): Fetched-{}, Filtered-{}\n'.format(
                self.totalTweets, filteredCount))
        else:
            self.logger.debug('writeToDB(): Fetched-{}, Filtered-{}\n'.format(
                self.totalTweets, 0))

    def __str__(self):
        """
        :return: String representation of the InvertedIndex
        """
        result = ""
        for idx in range(len(self.twitterHandles)):
            result += self.twitterHandles[idx] + ": " + str(len(self.indexLists[idx])) + "\n"
        return result
