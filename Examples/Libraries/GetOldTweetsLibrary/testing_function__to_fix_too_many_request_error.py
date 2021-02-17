import GetOldTweets3 as got
import time
import pandas as pd
from datetime import datetime, date, timedelta


def DownloadTweets(SinceDate, UntilDate, Query):
    """
    Downloads all tweets from a certain month in three sessions in order to avoid sending too many requests.
    Date format = 'yyyy-mm-dd'.
    Query=string.
    """
    since = datetime.strptime(SinceDate, "%Y-%m-%d")
    until = datetime.strptime(UntilDate, "%Y-%m-%d")
    tenth = since + timedelta(days=10)
    twentieth = since + timedelta(days=20)

    print("starting first download")
    first = (
        got.manager.TweetCriteria()
        .setQuerySearch(Query)
        .setSince(since.strftime("%Y-%m-%d"))
        .setUntil(tenth.strftime("%Y-%m-%d"))
    )
    firstdownload = got.manager.TweetManager.getTweets(first)
    firstlist = [[tweet.date, tweet.text] for tweet in firstdownload]

    df_1 = pd.DataFrame.from_records(firstlist, columns=["date", "tweet"])
    # df_1.to_csv("%s_1.csv" % SinceDate)

    time.sleep(600)

    print("starting second download")
    second = (
        got.manager.TweetCriteria()
        .setQuerySearch(Query)
        .setSince(tenth.strftime("%Y-%m-%d"))
        .setUntil(twentieth.strftime("%Y-%m-%d"))
    )
    seconddownload = got.manager.TweetManager.getTweets(second)
    secondlist = [[tweet.date, tweet.text] for tweet in seconddownload]

    df_2 = pd.DataFrame.from_records(secondlist, columns=["date", "tweet"])
    # df_2.to_csv("%s_2.csv" % SinceDate)

    time.sleep(600)

    print("starting third download")
    third = (
        got.manager.TweetCriteria()
        .setQuerySearch(Query)
        .setSince(twentieth.strftime("%Y-%m-%d"))
        .setUntil(until.strftime("%Y-%m-%d"))
    )
    thirddownload = got.manager.TweetManager.getTweets(third)
    thirdlist = [[tweet.date, tweet.text] for tweet in thirddownload]

    df_3 = pd.DataFrame.from_records(thirdlist, columns=["date", "tweet"])
    # df_3.to_csv("%s_3.csv" % SinceDate)

    df = pd.concat([df_1, df_2, df_3])
    df.to_csv("%s.csv" % SinceDate)

    return df
