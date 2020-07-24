import os
import pathlib
from typing import List

BASE_DIR: pathlib.Path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))

ALL_REDDIT_TAGS: List = ['work_from_home', 'social_distance', 'lockdown']
ALL_REDDIT_COLLETION_NAMES: List = ['corona_general', 'corona_countries',
                           'corona_regions', 'work_from_home',
                           'corona_states_with_tag']
ALL_SEARCH_TYPES = ['submission', 'comment']

ERROR_1 = 'responds are empty'
ERROR_2 = 'Expecting value: line 1 column 1 (char 0)'
KNOWN_ERROR = [ERROR_1, ERROR_2]
# MAX_AFTER = 166
MAX_AFTER = 30
