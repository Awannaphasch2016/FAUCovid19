#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""test_app_database"""

from global_parameters import PATH_TO_DATABASE


class TestRedditDatabase:

    def test_reddit_data_not_empty(self, reddit_cur):
        query = "select count(*) from reddit"
        reddit_cur.execute(query)
        num_data = reddit_cur.fetchone()[0]
        assert num_data > 0, f'{PATH_TO_DATABASE["reddit"]} is empty'


class TestTwitterDatabase:
    def test_twitter_data_not_empty(self, twitter_cur):
        query = "select count(*) from twitter"
        twitter_cur.execute(query)
        num_data = twitter_cur.fetchone()[0]
        assert num_data > 0, f'{PATH_TO_DATABASE["twitter"]} is empty'
