import GetOldTweets3 as got

from src.Utilities import my_timer


@my_timer
def run():
    tweetCriteria = (
        got.manager.TweetCriteria()
        .setQuerySearch("europe refugees")
        .setSince("2015-05-01")
        .setUntil("2015-09-30")
        .setMaxTweets(100)
    )
    # .setMaxTweets(1000)

    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    # tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
    print(len(tweet))


if __name__ == "__main__":
    run()
