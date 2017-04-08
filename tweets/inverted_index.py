__author__ = "Kantha Girish", "Pankaj Uchil Vasant", "Samana Katti"


class InvertedIndex:
    """
    This class implements the inverted index logic to create inverted index on trending
    topics and tweets. In this case, the documents are the trends themselves and the
    termList will be Twitter handles(Twitter usernames). An entry of python-twitter's
    `Status` object, which is the Tweet, is added to the postings list against each trend
    for each user, if he has tweeted under the trend.
    """
    __slots__ = ["twitterHandles", "trends", "indexLists"]

    def __init__(self, tweets):
        self.twitterHandles = []
        self.trends = []
        self.indexLists = []

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
            for tweet in tweets[trendName]:
                if tweet.user.screen_name not in self.twitterHandles:
                    self.twitterHandles.append(tweet.user.screen_name)
                    posts = [(self.trends.index(trendName), tweet)]
                    self.indexLists.append(posts)
                else:
                    posts = self.indexLists[self.twitterHandles.index(tweet.user.screen_name)]
                    posts.append((self.trends.index(trendName), tweet))

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
        :param targetHandles: A python dictionary of target twitter handles of popular
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

    def __str__(self):
        """
        :return: String representation of the InvertedIndex
        """
        result = ""
        for idx in range(len(self.twitterHandles)):
            result += self.twitterHandles[idx] + ": " + str(len(self.indexLists[idx])) + "\n"
        return result
