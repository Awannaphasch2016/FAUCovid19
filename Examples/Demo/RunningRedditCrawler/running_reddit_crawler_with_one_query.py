import datetime
import datetime as dt
# import json
import inspect
import logging
import os
import pathlib
from itertools import product
from typing import List
from typing import Tuple

from Examples.Libraries.PSAWLibrary.test_psaw_example_from_github import \
    _are_all_reponse_data_returned
from global_parameters import ALL_ASPECTS
from global_parameters import ALL_CRAWLERS
from global_parameters import ALL_REDDIT_COLLECTION_NAMES
from global_parameters import BASE_DIR
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
from src.Utilities import get_saved_file_path
from src.Utilities import save_to_file
from src.Utilities.CheckConditions.check_conditions import \
    check_running_conditions

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

LOGGER.info(f"{inspect.currentframe().f_code.co_name} is running ...")

# collection_name = corona_general & aspect = 'work_from_home'
# start_epoch = int(dt.datetime(2020, 9, 1).timestamp()),  # 49
# start_epoch = int(dt.datetime(2020, 10, 1).timestamp()),  # 24
# start_epoch = int(dt.datetime(2021, 10, 1).timestamp()),  # 0

# =====================
# == prepare param
# =====================


# collection_name = corona_general & aspect = 'social_distance'
year = 2020
month = 9
date = 1
# date = 5

start_epoch = int(dt.datetime(year, month, date).timestamp())

timestamp = datetime.datetime.now()


def get_file_name():
    file_name = f'total_number_of_data_from_{year}-{month}-{date}_' \
                f'to_{timestamp.year}-{timestamp.month}-{timestamp.day}.txt'
    return file_name


save_file = get_file_name()
save_path = pathlib.Path(os.getcwd())

reddit_crawler = 'reddit'
assert reddit_crawler == ALL_CRAWLERS[1]

# # kind = ALL_PSAW_SEARCH_KINDS
# # aspect = ALL_ASPECTS
# kind = ALL_PSAW_SEARCH_KINDS[1]
# # aspect = ALL_ASPECTS[0]
# aspect = ALL_ASPECTS[1]
# collection_name = ALL_REDDIT_COLLECTION_NAMES[0]


# for kind, aspect, collection_name in product(ALL_PSAW_SEARCH_KINDS,
#                                              ALL_ASPECTS,
#                                              ALL_REDDIT_COLLECTION_NAMES[:-1]
#                                              ):
all_data_to_save = []
all_params_tuple: List[Tuple] = list(product(ALL_PSAW_SEARCH_KINDS,
         ALL_ASPECTS,
         ALL_REDDIT_COLLECTION_NAMES[:-1]
         ))
all_params_tuple = all_params_tuple[-11:]

for kind, aspect, collection_name in all_params_tuple:

    # kind = "submission"
    # aspect = 'social_distance'
    # collection_name = 'corona_regions'

    LOGGER.info(f"kind = {kind}, aspect = {aspect},"
                f"collection_name = {collection_name}")

    # =====================
    # == Run program
    # =====================

    all_running_conditions = get_crawler_running_conditions(
        None,
        None,
        MAX_AFTER,
        [aspect],
        reddit_crawler,
    )

    # (condition_keys, running_conditions) = all_running_conditions[0]
    # # (condition_keys, running_conditions) = all_running_conditions[1]
    # check_running_conditions(running_conditions)
    # run_crawler_func, crawler_condition = select_crawler_condition(
    #     running_conditions=running_conditions,
    #     timestamp=timestamp,
    # )

    for (condition_keys, running_conditions) in all_running_conditions:

        check_running_conditions(running_conditions)

        run_crawler_func, crawler_condition = select_crawler_condition(
            running_conditions=running_conditions,
            timestamp=timestamp,
        )

        if collection_name == \
                crawler_condition['collection_class']['name']:
            break

    sort: Sort = running_conditions['sort']
    subreddit: List[str] \
        = crawler_condition['collection_class']['collection']['subreddit']
    aspect: List[str] \
        = crawler_condition['collection_class']['collection']['aspect']
    query: List[str] \
        = crawler_condition['collection_class']['collection']['query']
    search_type: str = crawler_condition['search_type']
    respond_type: str = crawler_condition['respond_type']

    assert aspect in ALL_ASPECTS

    # =====================
    # == set test parameters and execucte test
    # =====================

    # max_response_cache = 5
    # repeat = 3

    max_response_cache = 1000
    repeat = float("inf")

    # max_response_cache = 50
    # repeat = 100

    # query_str = query[0]
    query_str = '|'.join(query)
    # query_str = 'distance learning'
    # query_str = 'working'
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

        q=query_str,

        # =====================
        # == variables that are overwirtten
        # =====================
        sort=sort,
        # frequency='day',
        # aggs="created_utc",
        # metadata="true",
    )

    # x = list(caches)[0]
    # data_to_save = f"{kind},{aspect},{collection_name} = {len(x)}"
    # print(data_to_save)
    # all_data_to_save.append(data_to_save)
    # save_to_file('\n'.join(all_data_to_save), save_path/save_file)

    save_path = BASE_DIR / f"Outputs/Data/"\
                             f"RedditCrawler/"\
                             f"{aspect}/"\
                             f"{collection_name}/"\
                             f"{search_type}/"\
                             f"{respond_type}"


    # NOTE: I just want to check amount of each aspect for 2 months
    total: List[Json]
    total_response_for_a_date: List[Json]
    all_full_day_response_data: List[Json]
    (all_full_day_response_data, total,
     len_saved_data) = _return_response_data_from_psaw(
        caches,
        repeat,
        max_response_cache,
        save_path,
        None,
    )
    if not _are_all_reponse_data_returned(total,
                                          max_response_cache,
                                          repeat):
        raise ValueError

    LOGGER.debug(f'len(all_full_day_response_data) ='
                 f' {len(all_full_day_response_data)}')
    LOGGER.debug(f'len(total) = {len(total)}')
    LOGGER.debug(f'len_saved_data = {len_saved_data}')

    LOGGER.info('complete')
