#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contain all global variables."""

import os
import pathlib
from typing import List

from typing_extensions import Literal

from src.Utilities import Sort

#=====================
#==Database
#=====================
DATABASE_TYPE: List[str] = ['sqlite', 'mysql']

MYSQL_PORT = 3306
MYSQL_HOST = "127.0.0.1"

#=====================
#==Reddit & Twitter
#=====================

PROJECT_NAME = "FAUCOVID19"
BASE_DIR: pathlib.Path = pathlib.Path(
    os.path.dirname(os.path.realpath(__file__))
)

# Data
DATA_DIR: pathlib.Path = (
        pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / "Data"
)

# sqlite database
REDDIT_DATABASE = str(
    DATA_DIR / "Processed" / pathlib.Path("reddit_database.db")
)

TWITTER_DATABASE = str(
    DATA_DIR / "Processed" / pathlib.Path("twitter_database.db")
)

PATH_TO_DATABASE = {
    "reddit": REDDIT_DATABASE,
    "twitter": TWITTER_DATABASE,
}

# General
ERROR_1 = "responds are empty"
ERROR_2 = "Expecting value: line 1 column 1 (char 0)"
KNOWN_ERROR = [ERROR_1, ERROR_2]

# BUG: for some reason CRAWLERS_NAME cannot be imported
CRAWLERS_NAME = Literal["twitter", "reddit"]

# Crawlers
ALL_CRAWLERS: List[Literal["twitter", "reddit"]] =\
    ["twitter", "reddit", "twitter_stream","reddit_stream"]

# Aspects keywords
# ALL_ASPECTS = [
#     "work_from_home",
#     "social_distance",
#     "lockdown",
#     "reopen",
#     "corona",
# ]
ALL_ASPECTS = [
    "work_from_home",
    "social_distance",
    "corona",
    "reopen",
    "lockdown",
]
LOCKDOWN_KEYWORDS = [
    "quarantine",
    "isolation",
    "quarantining",
    "lockdown",
    "isolate",
]
REOPEN_KEYWORDS = ["reopening", "reopen"]
SOCIAL_DISTANCE_KEYWORDS = ["social distance", "social distancing"]
WORK_FROM_HOME_KEYWORDS = [
    "distance learning",
    "work online",
    "remote work",
    "workonline",
    # "remote work",
    # "online learning",
]
COVID_KEYWORDS = ["covid", "corona", "sarscov2"]

ALL_KEYWORDS = (
        LOCKDOWN_KEYWORDS
        + REOPEN_KEYWORDS
        + SOCIAL_DISTANCE_KEYWORDS
        + WORK_FROM_HOME_KEYWORDS
        + COVID_KEYWORDS
)

# crawlers' responds metadata
RESPONSE_KEYS = ['data', 'aggs', 'metadata']
# Reddit
ALL_REDDIT_TAGS: List[str] = ALL_ASPECTS

ALL_REDDIT_COLLECTION_NAMES: List = [
    "corona_general",
    "corona_countries",
    "corona_regions",
    "corona_states_with_tag",
]
# ALL_REDDIT_SEARCH_TYPES = ["submission", "comment"]
ALL_REDDIT_SEARCH_TYPES = ["comment", "submission"]
ALL_REDDIT_RESPOND_TYPES = ["data"]
ALL_REDDIT_FEILDS = [
    "aspect",
    "created_utc",
    "search_type",
    "crawler",
    "frequency",
    "subreddit",
    "link_id",
    "parent_id",
    "title",
    "body",
    "id",
    "sentiment",
]

ALL_SUBREDDIT_REPRESETED_GENERAL_COVID_SUBREDDIT = ["Corona", "COVID19",
                                                    "China_Flu",
                                                    "coronavirus"]
ALL_SUBREDDIT_REPRESETED_COUNTRY_SUBREDDIT = ["CoronavirusUS", "coronavirusUK"]
ALL_SUBREDDIT_REPRESETED_REGION_COVID_SUBREDDIT = [
    "CoronavirusMidwest",
    "CoronavirusSouth",
    "CoronavirusSouthEast",
    "CoronavirusWest",
]

# --------List of USA States
ALL_SUBREDDIT_REPRESETED_STATES_COVID_SUBREDDIT = [
    "alabama",
    "alaska",
    "arizona",
    "arkansas",
    "california",
    "colorado",
    "connecticut",
    "delaware",
    "florida",
    "georgia",
    "hawaii",
    "idaho",
    "illinois",
    "indiana",
    "iowa",
    "kansas",
    "kentucky",
    "louisiana",
    "maine",
    "maryland",
    "massachusetts",
    "michigan",
    "minnesota",
    "mississippi",
    "missouri",
    "montana",
    "nebraska",
    "nevada",
    "newhampshire",
    "newjersey",
    "newmexico",
    "newyork",
    "northcarolina",
    "northdakota",
    "ohio",
    "oklahoma",
    "oregon",
    "pennsylvania",
    "rhodeisland",
    "southcarolina",
    "southdakota",
    "tennessee",
    "texas",
    "utah",
    "vermont",
    "virginia",
    "washington",
    "westvirginia",
    "wisconsin",
    "wyoming",
]

REDDIT_META_DATA_KEYS = [
    "total_results",
    "before",
    "after",
    "frequency",
    "execution_time_milliseconds",
    "sort",
    "fields",
    "subreddit",
]

STREAM_COMMENTS_DATA_KEYS = [
    'author',
    'body',
    'body_html',
    'created_utc',
    # # NOTE: for distinguished, its type if Nonetype, and I don't know how to
    # #  check it because
    # #  this NoneType is not the same as None
    # 'distinguished',
    'edited',
    'id',
    'is_submitter',
    'link_id',
    'parent_id',
    'permalink',
    'replies',
    'score',
    'stickied',
    'submission',
    'subreddit',
    'subreddit_id',
]

# MAX_AFTER = 166
MAX_AFTER = 30
REDDIT_SORT: List[Sort] = ['asc', 'desc']

# NOTE: Twitter
#  >Keywords are copied from 'Tracking Social Media Discourse About the COVID-19 Pandemic: Developement of a Public Coronavirus  Twitter Dataset' github:
#  >https://github.com/echen102/COVID-19-TweetIDs/blob/master/keywords.txt

ALL_TWITTER_KEYWORDS: List = [
    "Coronavirus",
    "Corona",
    "Covid-19",
    "Corona virus",
    "Covid19",
    "Sars-cov-2",
    "COVID-19",
    "COVID",
    "Pandemic",
    "Coronapocalype",
    "CancelEverything",
    "Coronials",
    "SocialDistancing",
    "chinese virus",
    "stayhomechallenge",
    "DontBeaSpreader",
    "lockdown",
    "shelteringinplace",
    "staysafestayhome",
    "trumppandemic", "flatten the curve",
    "PPEshortage",
    "safeathome",
    "stayathome",
    "GetMePPE",
    "covidiot",
    "epitwitter",
    "Pandemie",
]

# ALL_TWITTER_HASHTAGS = None
ALL_TWITTER_TAGS: List[str] = ALL_ASPECTS

# NOTE: geo realted data is not implemented yet.
# ALL_TWITTER_COLLETION_NAMES: List = ['twitter_tweet', 'twitter_geo']
# ALL_TWITTER_SEARCH_TYPES = ['data_tweet', 'data_geo']
# ALL_TWITTER_RESPOND_TYPES = ['data_tweet', 'data_geo']

ALL_TWITTER_COLLETION_NAMES: List = ["twitter_tweet"]
ALL_TWITTER_SEARCH_TYPES = ["data_tweet"]
ALL_TWITTER_RESPOND_TYPES = ["data_tweet"]
ALL_TWITTER_FEILDS = [
    "crawler",
    "text",
    "date",
    "search_type",
    "aspect",
    "frequency",
    "sentiment",
    "id",
]

# Frequency
ALL_FREQUENCY = ["day"]
ALL_TWITTER_COVID_HASHTAGS = [
    "#coronavirus",
    "#coronavirusoutbreak",
    "#coronavirusPandemic",
    "#covid19",
    "#covid_19",
    "#epitwitter",
    "#ihavecorona",
]

if __name__ == '__main__':
    print('hi')
