import datetime
# import json
import inspect
import logging
from typing import List

from Examples.Libraries.PSAWLibrary.test_psaw_example_from_github import \
    _are_all_reponse_data_returned
from global_parameters import ALL_ASPECTS
from global_parameters import ALL_CRAWLERS
from global_parameters import MAX_AFTER
from src.Sources.Preparations.Data import get_crawler_running_conditions
from src.Sources.Preparations.Data import select_crawler_condition
from src.Sources.Preparations.Data.reddit_crawler import ALL_PSAW_SEARCH_KINDS
from src.Sources.Preparations.Data.reddit_crawler import \
    _return_response_data_from_psaw
from src.Sources.Preparations.Data.reddit_crawler import \
    get_response_data_with_psaw
from src.Utilities import Json
from src.Utilities import Sort
from src.Utilities.CheckConditions.check_conditions import \
    check_running_conditions
import datetime as dt

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

start_epoch = int(dt.datetime(2020, 9, 1).timestamp()),  # start_epoch
# kind = ALL_PSAW_SEARCH_KINDS
# aspect = ALL_ASPECTS
kind = ALL_PSAW_SEARCH_KINDS[1]
aspect = ALL_ASPECTS[0]


LOGGER.info(f"{inspect.currentframe().f_code.co_name} is running...")

# =====================
# == intialize query and subreddit for each aspect
# =====================

timestamp = datetime.datetime.now()

reddit_crawler = 'reddit'
assert reddit_crawler == ALL_CRAWLERS[1]

all_running_conditions = get_crawler_running_conditions(
    None,
    None,
    MAX_AFTER,
    [aspect],
    reddit_crawler,
)

(condition_keys, running_conditions) = all_running_conditions[0]

check_running_conditions(running_conditions)

run_crawler_func, crawler_condition = select_crawler_condition(
    running_conditions=running_conditions,
    timestamp=timestamp,
)

sort: Sort = running_conditions['sort']
subreddit: List[str] \
    = crawler_condition['collection_class']['collection']['subreddit']
aspect: List[str] \
    = crawler_condition['collection_class']['collection']['aspect']
query: List[str] \
    = crawler_condition['collection_class']['collection']['query']

assert aspect in ALL_ASPECTS

# =====================
# == set test parameters and execucte test
# =====================
previous_response_num = -1

query_str: str = '|'.join(query)

# max_response_cache = 5
# repeat = 3


max_response_cache = 1000
repeat = 1
# repeat = float('inf')

# max_response_cache = 1000
# repeat = 1

LOGGER.debug(f'query_str = {query_str}')

caches = get_response_data_with_psaw(
    max_response_cache=max_response_cache,
    kind=kind,
    is_full_response=False,

    after=start_epoch,
    subreddit=subreddit,
    # filter=filter,

    # =====================
    # == variable that may cause error
    # =====================

    # q=query[:2],
    q=query_str,

    # =====================
    # == variables that are overwirtten
    # =====================

    sort=sort,
    # frequency='day',
    # aggs="created_utc",
    # metadata="true",
)

total: List[Json]
total_response_for_a_date: List[Json]
all_full_day_response_data: List[Json]
(all_full_day_response_data, total, len_saved_data) = \
    _return_response_data_from_psaw(
        caches,
        repeat,
        max_response_cache,
        None,
        None,
    )


if not _are_all_reponse_data_returned(total,
                                      max_response_cache,
                                      repeat):
    raise ValueError

LOGGER.info('complete')
