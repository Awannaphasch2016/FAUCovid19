import sqlite3

import pytest

from global_parameters import PATH_TO_DATABASE
from src.Services.RedditTwitterDataAPI \
    .reddit_twitter_data_api_with_sqlite import app


@pytest.fixture(scope="module")
def reddit_cur():
    print("-----------connect to reddit database---------")
    conn = sqlite3.connect(PATH_TO_DATABASE["reddit"])
    cur = conn.cursor()
    yield cur
    print("-----------close connection to reddit database---------")
    conn.close()


@pytest.fixture(scope="module")
def twitter_cur():
    print("-----------connect to twitter database---------")
    conn = sqlite3.connect(PATH_TO_DATABASE["twitter"])
    cur = conn.cursor()
    yield cur
    print("-----------close connection to twitter database---------")
    conn.close()

@pytest.fixture
def client():
    # Prepare before your test
    with app.test_client() as client:
        # Give control to your test
        yield client
