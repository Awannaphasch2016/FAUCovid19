#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""test_app_database"""

import pytest
import sqlite3

from global_parameters import DATA_DIR

path_to_database = {
    "reddit": str(DATA_DIR / "Processed/reddit_database.db"),
    "twitter": str(DATA_DIR / "Processed/twitter_database.db"),
}


@pytest.fixture(scope="module")
def reddit_cur():
    print("-----------connect to reddit database---------")
    conn = sqlite3.connect(path_to_database["reddit"])
    cur = conn.cursor()
    yield cur
    print("-----------close connection to reddit database---------")
    conn.close()


@pytest.fixture(scope="module")
def twitter_cur():
    print("-----------connect to twitter database---------")
    conn = sqlite3.connect(path_to_database["twitter"])
    cur = conn.cursor()
    yield cur
    print("-----------close connection to twitter database---------")
    conn.close()


class TestRedditDatabase:

    def test_reddit_data_not_empty(self, reddit_cur):
        query = "select count(*) from reddit"
        reddit_cur.execute(query)
        num_data = reddit_cur.fetchone()[0]
        assert num_data > 0, f'{path_to_database["reddit"]} is empty'


class TestTwitterDatabase:
    def test_twitter_data_not_empty(self, twitter_cur):
        query = "select count(*) from twitter"
        twitter_cur.execute(query)
        num_data = twitter_cur.fetchone()[0]
        assert num_data > 0, f'{path_to_database["twitter"]} is empty'
