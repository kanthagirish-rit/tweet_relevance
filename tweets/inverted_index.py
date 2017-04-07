__author__ = "Kantha Girish"


class InvertedIndex:
    """
    """
    __slots__ = ["twitterHandles", "trends", "indexLists"]

    def __init__(self, tweets):
        self.twitterHandles = []
        self.trends = []
        self.indexLists = []

        self._populate(tweets)

    def _populate(self, tweets):
        """
        :param tweets:
        :return:
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
        :param handle:
        :return:
        """
        if handle in self.twitterHandles:
            return self.indexLists[self.twitterHandles.index(handle)]
        else:
            return []

    def getRelevantTweets(self, targetHandles):
        """
        :param targetHandles:
        :return:
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
        :return:
        """
        result = ""
        for idx in range(len(self.twitterHandles)):
            result += self.twitterHandles[idx] + ": " + str(len(self.indexLists[idx])) + "\n"
        return result
