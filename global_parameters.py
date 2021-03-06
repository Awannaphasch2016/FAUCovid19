import os
import pathlib
from typing import List

BASE_DIR: pathlib.Path = pathlib.Path(
os.path.dirname(os.path.realpath(__file__)))
# General
ERROR_1 = 'responds are empty'
ERROR_2 = 'Expecting value: line 1 column 1 (char 0)'
KNOWN_ERROR = [ERROR_1, ERROR_2]


# Aspects keywords
ALL_ASPECTS = ['work_from_home', 'social_distance', 'lockdown', 'reopen', 'corona']
LOCKDOWN_KEYWORDS = ['quarantine', 'isolation',
                        'quarantining', 'lockdown', 'isolate']
REOPEN_KEYWORDS = ['reopening', 'reopen']
SOCIAL_DISTANCE_KEYWORDS = ['social distance', 'social distancing']
WORK_FROM_HOME_KEYWORDS = ['remote work', 'workonline', 'work online'
                            'remote work', 'online learning', 'distance learning']
COVID_KEYWORDS = ['covid', 'corona', 'sarscov2']

ALL_KEYWORDS = LOCKDOWN_KEYWORDS + REOPEN_KEYWORDS +  SOCIAL_DISTANCE_KEYWORDS +  WORK_FROM_HOME_KEYWORDS + COVID_KEYWORDS

# Reddit
ALL_REDDIT_TAGS: List = ALL_ASPECTS

ALL_REDDIT_COLLECTION_NAMES: List = ['corona_general', 'corona_countries',
                                    'corona_regions', 
                                    'corona_states_with_tag']
ALL_REDDIT_SEARCH_TYPES = ['submission', 'comment']
ALL_REDDIT_RESPOND_TYPES = ['data']

# MAX_AFTER = 166
MAX_AFTER = 30

# Twitter Note:
#  >Keywords are copied from 'Tracking Social Media Discourse About the COVID-19 Pandemic: Developement of a Public Coronavirus  Twitter Dataset' github:
#  >https://github.com/echen102/COVID-19-TweetIDs/blob/master/keywords.txt

ALL_TWITTER_KEYWORDS: List = ['Coronavirus', 'Corona',
                              'Covid-19', 'Corona virus', 'Covid19',
                              'Sars-cov-2',
                              'COVID-19', 'COVID', 'Pandemic', 'Coronapocalype',
                              'CancelEverything', 'Coronials', 'SocialDistancing',
                              'chinese virus', 'stayhomechallenge',
                              'DontBeaSpreader', 'lockdown', 'shelteringinplace', 'staysafestayhome',
                              'trumppandemic', 'flatten the curve', 'PPEshortage', 'safeathome','stayathome',
                              'GetMePPE', 'covidiot', 'epitwitter','Pandemie'
                              ]

# ALL_TWITTER_HASHTAGS = None
ALL_TWITTER_TAGS: List = ALL_ASPECTS

# NOTE: geo realted data is not implemented yet.
# ALL_TWITTER_COLLETION_NAMES: List = ['twitter_tweet', 'twitter_geo']
# ALL_TWITTER_SEARCH_TYPES = ['data_tweet', 'data_geo']
# ALL_TWITTER_RESPOND_TYPES = ['data_tweet', 'data_geo']

ALL_TWITTER_COLLETION_NAMES: List = ['twitter_tweet'] 
ALL_TWITTER_SEARCH_TYPES = ['data_tweet']
ALL_TWITTER_RESPOND_TYPES = ['data_tweet']


# this is new checkpoint Anak 'Wannaphaschaiyong'
# this is not in checkpoint 













