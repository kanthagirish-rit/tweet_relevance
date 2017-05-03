"""
description: extract tweets for trends and save to database, to create models for
classification
"""

from populate_feed import getTweets


def main():
    """
    :return: None

    This function fetches tweets for a list of woeids and combines all the tweets for a trend
    into a single document and the file is saved after the name of the trend. The resulting
    files serve as the documents which are manually classified into categories and can be
    used for training a classifier.
    """
    woeid = [2450022, 2487796, 2487889]
    # NYC:2459115, LA:2442047, Miami:2450022,
    # SA:2487796, SD:2487889, SF:2487956
    # Seattle:2490383, SJ:2488042, bang:2295420
    # Austin:2357536

    for id in woeid:
        tweets = getTweets(id)

        folder = "/home/kantha/RIT/kpt/project/tweets/" + str(id) + "/01/"
        for trend in tweets:
            if len(tweets[trend]) > 0:
                with open(folder+"trend_"+trend+".txt", 'w') as file:
                    file.write("\n\n".join([t.text.strip() for t in tweets[trend]]))

if __name__ == '__main__':
    main()
