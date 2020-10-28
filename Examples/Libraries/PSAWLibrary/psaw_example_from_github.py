#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# TODO:
#  > get 2 keys each from: data, aggs, and metadata
#  > print out a dict with all 3 keys and its value
import time

import praw
from psaw import PushshiftAPI

from credentials import REDDIT_CLIENT_ID
from credentials import REDDIT_CLIENT_SECRET
from credentials import REDDIT_PASSWORD
from credentials import REDDIT_USERNAME
from credentials import REDDIT_USER_AGENT
from src.Utilities import my_timer

r = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                password=REDDIT_PASSWORD,
                user_agent=REDDIT_USER_AGENT,
                username=REDDIT_USERNAME)

api = PushshiftAPI(r)

import datetime as dt

start_epoch = int(dt.datetime(2017, 1, 1).timestamp())


def get_first_10_submission(start_epoch):

    x = list(api.search_submissions(after=start_epoch,
                                    subreddit='politics',
                                    filter=['url',
                                            'author',
                                            'title',
                                            'subreddit'],
                                    limit=1000))

    return x

def get_first_10_submission1(start_epoch):

    x = list(api.search_submissions(after=start_epoch,
                                    subreddit='politics',
                                    limit=1000))

    return x

@my_timer
def func3():


    gen = list(api.search_submissions(after=start_epoch,
                                    subreddit='politics',
                                    limit=1000))


    # gen = api.search_submissions(after=start_epoch,
    #                                 # subreddit='politics',
    #                                 subreddit=['politics','askreddit'],
    #                                 filter=['url',
    #                                         'author',
    #                                         'title',
    #                                         'subreddit'],
    #                              # )
    #                                 limit=1000)

    # gen = api.search_comments(q='OP', subreddit='askreddit')

    max_response_cache = 111
    # max_response_cache = float('inf')
    cache = []

    s = time.time()
    for c in gen:
        cache.append(c)

        # Omit this test to actually return all results. Wouldn't recommend it though: could take a while, but you do you.
        if len(cache) >= max_response_cache:
            break

    return cache

if __name__ == '__main__':

    # print(len(get_first_10_submission1(start_epoch)))
    print(len(func3()))



