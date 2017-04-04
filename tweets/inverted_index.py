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
                    posts = [tweet]
                    self.indexLists.append(posts)
                else:
                    posts = self.indexLists[self.twitterHandles.index(tweet.user.screen_name)]
                    posts.append(tweet)

    def search(self, handle):
        """
        :param handle:
        :return:
        """
        if handle in self.twitterHandles:
            return self.indexLists[self.twitterHandles.index(handle)]
        else:
            return []
