# -*- coding: utf-8 -*-

"""Prepare and crawl Reddit data."""

import datetime
import json
import pathlib
import time
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from typing import cast

import deprecation  # type: ignore
import numpy as np  # type: ignore
import praw  # type: ignore
import requests
from psaw import PushshiftAPI  # type: ignore
from tqdm import tqdm  # type: ignore
from typing_extensions import TypedDict

from credentials import REDDIT_CLIENT_ID
from credentials import REDDIT_CLIENT_SECRET
from credentials import REDDIT_PASSWORD
from credentials import REDDIT_USERNAME
from credentials import REDDIT_USER_AGENT
from global_parameters import ALL_REDDIT_TAGS
from global_parameters import BASE_DIR
from global_parameters import KNOWN_ERROR
from global_parameters import REDDIT_META_DATA_KEYS
from global_parameters import RESPONSE_KEYS
from src import __version__
from src.Sources.Preparations.Features.sentiment_analysis import get_sentiment
from src.Utilities import ControlLimit
from src.Utilities import Frequency
from src.Utilities import Json
from src.Utilities import Query
from src.Utilities import RedditMetadata
from src.Utilities import RedditResponse
from src.Utilities import RedditRunningConstraints
from src.Utilities import SubredditCollection
from src.Utilities import Tags
from src.Utilities import Url
from src.Utilities import (
    _ensure_datetime_for_specified_frequency_not_consider_max_after,
)
from src.Utilities import get_saved_file_path
from src.Utilities import get_saved_file_path_for_1_full_day
from src.Utilities import my_timer
from src.Utilities import only_download_full_day
from src.Utilities import save_to_file
from src.Utilities.CheckConditions.check_conditions import check_response_keys
from src.Utilities.CheckConditions.check_conditions import \
    check_that_all_selected_fields_are_returns
from src.Utilities.Generator.generator_utilities import peek
from src.Utilities.Logging import MyLogger
from src.Utilities.time_utility import (
    _convert_timedelta_to_specified_frequency,
)
from src.Utilities.time_utility import _get_epoch_datetime_subtract_timedelta

LOGGER = MyLogger()
PROGRAM_LOGGER = LOGGER.program_logger

ALL_PSAW_SEARCH_KINDS = ['submission', 'comment']

r = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                password=REDDIT_PASSWORD,
                user_agent=REDDIT_USER_AGENT,
                username=REDDIT_USERNAME)

psaw_api = PushshiftAPI(r)


def get_response_data_with_psaw(
        max_response_cache: int,
        kind: str,
        is_full_response: bool,
        **kwargs) -> Generator[List[Json], None, None]:
    def _check_input(_kwargs: Dict):

        if _kwargs.get('limit', None):
            raise ValueError("limit input is not allowed.: {_kwargs.get("
                             "'limit', None)}")

        if _kwargs.get('fields', None) is not None \
                or _kwargs.get('filter', None) is not None:
            raise ValueError(
                f"I decided that all fields should be retrived,"
                f" so I don't need to maintain 2 versions: 1) "
                f"from pushshift and 2) from my own database.")

        if _kwargs.get('aggs', None):
            raise ValueError("aggs will be ovewritten. Psaw does not "
                             "support aggs.")

        if _kwargs.get('metadata'):
            raise ValueError(
                "Metadata will be overwritte. Psaw always set "
                "Metadata to true")

        if _kwargs.get('frequency'):
            raise ValueError("Havnen't check frequency throughly but by "
                             "default. it seem that frequency is set to day.")

    def _is_search_full_response(_is_full_response):
        if _is_full_response:
            raise NotImplementedError("Deprecated. No longer in use.")
            if kind != 'full_response':
                raise ValueError
        else:
            if kind == 'full_response':
                raise ValueError

    def _search_comment_or_submission_or_full_response(_kind):

        if _kind == 'submission':
            # return api.search_submissions(q='OP', subreddit='askreddit')
            return psaw_api.search_submissions(**kwargs)
        elif _kind == 'comment':
            # return api.search_comments(q='OP', subreddit='askreddit')
            return psaw_api.search_comments(**kwargs)
        else:
            raise ValueError(
                'Only support search_submission or search_comment.'
            )

    _check_input(kwargs)
    _is_search_full_response(is_full_response)

    gen = _search_comment_or_submission_or_full_response(kind)

    PROGRAM_LOGGER.debug('get_response_data_with_psaw is running..')

    cache = []
    for c in gen:
        cache.append(c)
        if len(cache) >= max_response_cache:
            PROGRAM_LOGGER.debug(f"len(cache) = {len(cache)}")
            yield cache
            cache = []

    PROGRAM_LOGGER.debug(f'len(cache) =  + {len(list(cache))}')
    # return cache
    yield cache

def _return_response_data_from_psaw(caches: Generator[List[Json], None, None],
                                    _repeat: int,
                                    _max_response_cache,
                                    _save_path: pathlib.Path = None,
                                    _save_file: str = None,
                                    ) \
        -> Tuple[RedditResponse,List[Json], int]:
    """


    Note: I need to change the function name to match what it is doing.
        _send_requests should be only the section where
        `caches are being iterated`.
    """

    def _check_input_conpatibility() -> bool:
        count = 0
        if _save_path is not None:
            count += 1

        if count == 0:
            return False
        elif count == 1:
            return True
        else:
            raise ValueError

    is_saved = _check_input_conpatibility()

    total: List[Json] = []
    total_response_for_a_date: List[Json] = []

    def _get_reddit_data(response_data_key: List) -> Json:
        return {"data": response_data_key}

    def _get_date_func(i: int,
                       _current_total: List[Json]) -> Tuple[int, int]:

        utc_timestamp_full = _current_total[i]['created_utc']
        timestamp = datetime.datetime.fromtimestamp(
            utc_timestamp_full
        )
        year = timestamp.year
        month = timestamp.month
        day = timestamp.day

        utc_timestamp_day = datetime.datetime(year, month, day).timestamp()

        return utc_timestamp_day, utc_timestamp_full

    def _is_not_full_day(
            _first_date: int,
            _current_date: int) -> bool:
        assert _first_date >= _current_date

        if (_first_date - _current_date) == 0:
            return False

        return True

    def _detect_new_date(
            _current_total: List[Json],
            # first_date: int,
            # *args,
    ) -> Union[int, bool]:

        # print(f"frist_date = {first_date}")

        (first_date_in_current_total, _) = \
            _get_date_func(0, _current_total.copy())
        # print(f"first_date_in_current_total ="
        #       f" {first_date_in_current_total}")

        # print(f"len(_current_total) > 1 = {len(_current_total) > 1 }")

        if len(_current_total) > 1:
            previous_date = first_date_in_current_total

            for ind, _ in enumerate(_current_total):

                current_date: int
                (current_date, _) = _get_date_func(ind,
                                                   _current_total.copy())

                # if (current_date < first_date) \
                #         and (previous_date != current_date):
                if (current_date < first_date_in_current_total) \
                        and (previous_date != current_date):
                    PROGRAM_LOGGER.debug(f'ind = {ind}')
                    return ind

                previous_date = current_date
        return False

    left_ind = 0
    len_saved_data = 0
    num_non_full_day_data = 0
    count = 0
    # repeat_end_ind = _repeat - 1
    _repeat = _repeat
    first_full_day_data_ind = None

    # Note: This line allow nonlocal first_date in inner scope
    #   to bine with it
    cache: List[Json]
    is_terminated_before_all_caches_iteration = True


    s = time.time()
    for ind, cache in enumerate(caches):
        f = time.time()
        PROGRAM_LOGGER.info(f'time caches (generator) takes to return 1 cache = '
                    f'{f-s} seconds.')

        def _is_terminate_state():

            nonlocal ind
            nonlocal _repeat
            nonlocal is_terminated_before_all_caches_iteration
            nonlocal cache

            if ind == _repeat:
                is_terminated_before_all_caches_iteration = False

                return True

            if len(cache) <= 1:
                return True

            return False

        if _is_terminate_state():
            break

        if ind == 0:
            first_date: int
            first_date_full: int

            (first_date, first_date_full) = _get_date_func(0, cache.copy())

            def _is_sorted_order_correctly(_first_date_full: int):
                last_date_full: int
                (_, last_date_full) = _get_date_func(1, cache.copy())
                return (_first_date_full - last_date_full) > 0

            if len(cache) > 1:
                assert _is_sorted_order_correctly(first_date_full), \
                    "Data is sorted in 'desc' order, so first_date have " \
                    "to be more than second_date."


        # current_date: int
        # current_date_full: int
        # (current_date, current_date_full) = _get_date_func(ind, cache.copy())
        # if not _is_in_full_day_data(first_date,
        #                             current_date):
        #     num_non_full_day_data += len(cache)
        #     continue

        def is_first_full_day_ind_detected() -> bool:

            def has_full_day_data() -> bool:

                nonlocal cache
                nonlocal num_non_full_day_data
                nonlocal left_ind
                nonlocal first_full_day_data_ind

                for inner_ind, response_data in enumerate(cache):
                    current_date: int
                    current_date_full: int
                    (current_date, current_date_full) = \
                        _get_date_func(inner_ind, cache.copy())

                    if _is_not_full_day(first_date,
                                        current_date):
                        num_non_full_day_data += 1
                        continue
                    else:
                        # TODO: why + 1?
                        left_ind += (num_non_full_day_data + 1)
                        first_full_day_data_ind = left_ind

                        # print("left_ind", left_ind)
                        # print("num_non_full_day_data", num_non_full_day_data)
                        # print(_get_date_func(0, cache)[1])
                        # print(_get_date_func(left_ind - 1, cache)[1])

                        assert _get_date_func(0, cache)[1] > \
                               _get_date_func(left_ind, cache)[1]
                        assert _get_date_func(0, cache)[1] == \
                               _get_date_func(left_ind - 1, cache)[1]

                        return True
                return False

            if left_ind == 0:
                is_detected = has_full_day_data()
                return is_detected

            return True

        if not is_first_full_day_ind_detected():
            continue

        total_response_for_a_date += cache
        total += cache

        # print(f'ind = {ind}')
        # print(f"len(cache) = {len(cache)}")
        # print(f"len(total) = {len(total)}")

        is_detected_ind = \
            _detect_new_date(total_response_for_a_date)

        if is_detected_ind:
            right_ind = left_ind + is_detected_ind
            response: Json = \
                _get_reddit_data(
                    total[left_ind:right_ind])
            len_saved_data += len(response['data'])


            # if is_saved:
            #     _save_path_ = _save_path / f"{_save_file}"
            #     _save_path_ = \
            #         pathlib.Path(str(_save_path_).format(ind))
            #     save_to_file(response, _save_path_)

            if is_saved:

                if _save_file is None:
                    _save_file_path: pathlib.Path = \
                        get_saved_file_path_for_1_full_day(
                        datetime.datetime.fromtimestamp(
                            _get_date_func(0, total_response_for_a_date)[1]
                        ),
                        path_name=_save_path,
                    )


                    # def _get_unique_file_name():
                    #     _save_file: str = str(_save_file_path).split('/')[-1]
                    #     _save_path: pathlib.Path =\
                    #         pathlib.Path(
                    #             '/'.join(str(_save_file_path).split('/')[:-1])
                    #         )
                    #
                    #     file_name_suffix: int = 0
                    #     unique_file_name = _save_file + str(file_name_suffix)
                    #     while True:
                    #         if pathlib.Path(
                    #                 str(_save_path/unique_file_name)
                    #         ).exists():
                    #             file_name_suffix += 1
                    #         else:
                    #             break
                    # _save_path_: pathlib.Path = _save_path/ unique_file_name

                    _save_path_: pathlib.Path = _save_file_path
                save_to_file(response, _save_path_)
                PROGRAM_LOGGER.info(f'len_saved_data = {len_saved_data}')

            total_response_for_a_date = \
                total[right_ind:]
            left_ind = right_ind

    def _is_data_iterated_correctly(
            _ind: int,
            __repeat: int,
            _is_terminated_before_all_caches_iteration: bool,
    ) -> bool:

        num_full_day_total = len(total) + num_non_full_day_data

        # Note: when len of returned response is exactly repeat_end_ind *
        #   _max_response_cache, in that casue _ind == repeat_end_ind -1.
        #   However, in the case where terminal_state is executed (
        #   returned response > max_response_cache * repeat_end_ind )
        #   response <= max_response_cache * repeat_end_ind

        if _is_terminated_before_all_caches_iteration:
            assert _ind < _repeat

        else:

            assert _ind == _repeat

        assert num_full_day_total > _max_response_cache * (
                _repeat - 1)
        return num_full_day_total <= _max_response_cache * _repeat

    def is_data_saved_correctly() -> bool:

        try:
            # TODO: fix?
            return right_ind - first_full_day_data_ind == len_saved_data
        except:
            return len_saved_data == 0

    try:
        assert _is_data_iterated_correctly(
            ind,
            _repeat,
            is_terminated_before_all_caches_iteration,
        )
    except:
        try:
            tmp = next(caches)
            # tmp = next(caches)
        except StopIteration as e:
            PROGRAM_LOGGER.warning("caches is empty from the beginning. ")
        except Exception as e:
            raise e

    # print('hi')
    # exit()

    assert is_data_saved_correctly()

    # NOTE: paragraph of code below take care of a case where each
    #  iteriation of cache may contains more than 2 different dates.
    #  -
    #  In this case, after for loop is complete,
    #  we need to save the data of a full date because len(
    #  total_response_for_a_date) will be more than 0 and it may also
    #  contain more than 1 dates.

    PROGRAM_LOGGER.debug(f"len(total_response_for_a_date) = "
                 f"{len(total_response_for_a_date)}")

    if len(total_response_for_a_date) > 0:

        PROGRAM_LOGGER.debug(total_response_for_a_date)

        left_ind = 0

        leftover_total: List[Json] = total_response_for_a_date

        last_detected_ind = -999

        response_data: Json
        for ind, response_data in enumerate(leftover_total):

            current_date: int
            (current_date, _) = \
                _get_date_func(ind, leftover_total.copy())

            if left_ind == 0:
                current_date: int
                current_date_full: int
                (current_date, current_date_full) = \
                    _get_date_func(ind, leftover_total.copy())
                if _is_not_full_day(first_date,
                                    current_date):
                    num_non_full_day_data += 1
                    continue
                else:
                    left_ind += (num_non_full_day_data + 1)

                    # print("left_ind", left_ind)
                    # print("num_non_full_day_data", num_non_full_day_data)
                    # print(_get_date_func(0, cache)[1])
                    # print(_get_date_func(left_ind - 1, cache)[1])

                    assert _get_date_func(0, cache)[1] > \
                           _get_date_func(left_ind, cache)[1]
                    assert _get_date_func(0, cache)[1] == \
                           _get_date_func(left_ind - 1, cache)[1]

            is_detected_ind = \
                _detect_new_date(total_response_for_a_date)
            # _detect_new_date(total_response_for_a_date, first_date)

            if is_detected_ind:
                last_detected_ind = ind

                right_ind = left_ind + is_detected_ind
                response: Json = \
                    _get_reddit_data(
                        leftover_total[left_ind:right_ind])

                len_saved_data += len(response)

                # if is_saved:
                #     _save_path_ = _save_path / f"{_save_file}"
                #     _save_path_ = \
                #         pathlib.Path(str(_save_path_).format(ind))
                #     save_to_file(response, _save_path_)

                if is_saved:

                    if _save_file is None:
                        _save_file_path: pathlib.Path = \
                            get_saved_file_path_for_1_full_day(
                                datetime.datetime.fromtimestamp(
                                    _get_date_func(0,
                                                   total_response_for_a_date)[
                                        1]
                                ),
                                path_name=_save_path,
                            )

                        # def _get_unique_file_name():
                        #     _save_file: str = str(_save_file_path).split('/')[-1]
                        #     _save_path: pathlib.Path =\
                        #         pathlib.Path(
                        #             '/'.join(str(_save_file_path).split('/')[:-1])
                        #         )
                        #
                        #     file_name_suffix: int = 0
                        #     unique_file_name = _save_file + str(file_name_suffix)
                        #     while True:
                        #         if pathlib.Path(
                        #                 str(_save_path/unique_file_name)
                        #         ).exists():
                        #             file_name_suffix += 1
                        #         else:
                        #             break
                        # _save_path_: pathlib.Path = _save_path/ unique_file_name

                        _save_path_: pathlib.Path = _save_file_path
                    save_to_file(response, _save_path_)
                    PROGRAM_LOGGER.info(f'len_saved_data = {len_saved_data}')

                total_response_for_a_date = \
                    leftover_total[right_ind:]
                left_ind = right_ind

            def _is_terminal_state(_ind: int,
                                   _last_detected_ind: ind,
                                   _total_response_for_a_date: List[Json],
                                   ):

                return (_ind - _last_detected_ind) > \
                       len(_total_response_for_a_date)

            if _is_terminal_state(ind,
                                  last_detected_ind,
                                  total_response_for_a_date):
                break

    all_full_day_response_data: List[Json] = total[:num_non_full_day_data]
    all_full_day_response: RedditResponse = {
        i: None for i in RESPONSE_KEYS
    }
    def _ensure_response_keys():
        nonlocal all_full_day_response

        for i in RESPONSE_KEYS:
            if all_full_day_response.get(i, None) is None:
                if i == RESPONSE_KEYS[0]:
                    all_full_day_response[i] = all_full_day_response_data
                else:
                    all_full_day_response[i] = {}

    _ensure_response_keys()


    return all_full_day_response, total, len_saved_data



class RedditCrawler:
    """This class will prepare and crawl data from reddit."""

    def __init__(
            self,
            subreddits_collection_class: SubredditCollection,
            respond_type: str,
            search_type: str,
            frequency: Frequency,
            verbose: int,
            aspect: str,
            max_after: int,
    ):
        """Skipped summary."""
        self.crawler_name = "RedditCrawler"
        self.verbose = verbose
        self.prepare_crawler(
            subreddits_collection_class,
            respond_type,
            search_type,
            frequency,
            aspect,
            max_after,
        )

    def prepare_crawler(
            self,
            subreddits_collection_class: SubredditCollection,
            respond_type: str,
            search_type: str,
            frequency: Frequency,
            aspect: Union[str, Tuple[str]],  # VALIDATE: hat is the correct
            # Type.
            max_after: int,
    ) -> None:
        """
        Prepare common data that will be used among class's methods.

        :type subreddits_collection_class:  SubredditCollection
        :param subreddits_collection_class: Dict contains info about collection
         of data that will be crawled

        :type respond_type: str
        :param respond_type: desired respond type by crawler

        :type search_type: str
        :param search_type: desired search type by crawler

        :type frequency: Frequency
        :param frequency: interval of time to retrieved data

        :type aspect: str
        :param aspect: any specified aspect

        :param max_after: int
        :param max_after: number of (previous) frequency that will be collected

        """
        self.search_type = search_type
        self.frequency = frequency
        self.collection_name = subreddits_collection_class["name"]
        self.collection = subreddits_collection_class["collection"]
        self.aspect = aspect
        self.query = self.collection["query"]
        self.subreddit = self.collection['subreddit']
        self.max_after = max_after
        self.respond_type = respond_type

    def prepare_running_crawler(
            self,
            before: Optional[int],
            after: int,
            max_after: int,
    ) -> RedditRunningConstraints:
        """Skipped summary.

        Prepare dict constraints that will be used to run (crawl) data for each
             iteration.

        :type before: None or int
        :param before: date in which all aata BEFORE this date should be
            retrieved

        :type after: int
        :param after: date in which all aata AFTER this date should be
            retrieved

        :param max_after: int
        :param max_after: number of (previous) frequency that will be collected

        :rtype:  RedditRunningConstraints
        :return: dict of constraint that will be used to run (crawl) data
        """
        common_fields = (
            "author, author_flair_richtext, author_flair_type, "
            "author_fullname,id, created_utc, permalink, "
            "retrieved_on, score, subreddit, subreddit_id, "
            "total_awards_received, stickied, all_awardings"
        )

        subreddit_fields = (
            " domain, full_link, is_original_content, "
            "is_self, num_comments, pinned, selftext, "
            "subreddit_subscribers, title, upvote_ratio"
        )

        comment_fields = "body,parent_id,link_id"
        max_response_cache = 20
        # repeat = float('inf')  # no limit
        repeat = 1  # to test that that demo works

        now = datetime.datetime.now()
        self.timestamp_utc = _get_epoch_datetime_subtract_timedelta(
            now,
            self.frequency,
            after,
        )

        max_after_timestamp_utc = _get_epoch_datetime_subtract_timedelta(
            now,
            "day",
            max_after,
        )

        # FIXME: fix this error
        assert (
                self.timestamp_utc >= max_after_timestamp_utc
        ), f"{self.timestamp_utc}, {max_after_timestamp_utc}, {after}"

        def replace_and_split(x):
            return x.replace(" ", "").split(",")

        fields = (
                replace_and_split(common_fields)
                + replace_and_split(subreddit_fields)
                + replace_and_split(comment_fields)
        )
        fields = ",".join(fields)

        running_constraints: RedditRunningConstraints
        running_constraints = {
            "before": before,
            "after": after,
            "aggs": "created_utc",
            "size": 1000,
            "metadata": "true",
            "sort": "asc",
            "fields": fields,
            "max_response_cache": max_response_cache,
            "repeat": repeat,
        }

        if self.frequency == "day":
            self.time_since = (
                    datetime.datetime.now().date() - datetime.timedelta(
                days=after)
            )

            if before is not None:
                self.time_until = (
                        datetime.datetime.now().date()
                        - datetime.timedelta(days=before)
                )

            else:
                self.time_until = datetime.datetime.now().date()
        else:
            raise NotImplementedError

        self.current_condition_str = (
            f" aspect = {self.aspect} -> query = {self.query}"
            f"||collection_name = {self.collection_name} "
            f"|| search_type = {self.search_type} "
            f"|| respond_type = {self.respond_type}"
            f"|| frequency = {self.frequency} "
            f"|| {after} <= x < {before} "
            f"|| {str(self.time_since)} to {str(self.time_until)}"
        )

        if self.verbose:
            PROGRAM_LOGGER.info(f" {self.current_condition_str}")

        return running_constraints

    def get_url(self, running_constraints: RedditRunningConstraints) -> Url:
        """
        Prepare variable + get url with selected parameters.

        :type running_constraints: RedditRunningConstraints
        :param running_constraints: Dict contains keys that determines contains
         before running a crolwer

        :rtype:  Url
        :return: url with selected parameters
        """
        # frequency = running_constraints['frequency']
        before = running_constraints["before"]

        def _get_after_frequency():
            if self.frequency == "day":
                after_frequency = "d"
            elif self.frequency == "hour":
                after_frequency = "h"
            elif self.frequency == "minute":
                after_frequency = "m"
            elif self.frequency == "second":
                after_frequency = "s"
            else:
                raise NotImplementedError
            return after_frequency

        after_frequency = _get_after_frequency()

        if self.aspect is None:
            endpoint_url = self._get_url_endpoint_without_query_param(
                running_constraints,
                after_frequency,
            )
        elif self.aspect in ALL_REDDIT_TAGS:
            endpoint_url = self._get_url_endpoint_with_query_param(
                running_constraints,
                after_frequency,
            )
        else:
            raise NotImplementedError

        if before is not None:
            endpoint_url += f"&before={before}{after_frequency}"

        return endpoint_url



    @my_timer
    # @signature_logger
    def get_responds(
            self,
            running_constraints: RedditRunningConstraints,
    ) -> RedditResponse:
        """Skipped summary.

        Prepare varaibles to be pass in (ANY) api and prepare output from (ANY)
         api.

        :type running_constraints: RedditRunningConstraints
        :param running_constraints: Dict contains keys that determines contains
         before running a crolwer

        :rtype: None or Json
        :return: respond data with appropriate respond key format
        """
        before = running_constraints["before"]
        after = running_constraints["after"]
        sort = running_constraints["sort"]
        max_response_cache = running_constraints["max_response_cache"]
        repeat = running_constraints["repeat"]

        # VALIDATE: This function doesn't  make much sense. try to fix/check
        #  it in the future
        only_download_full_day(self.frequency, before, after)


        def ensure_json(res) -> RedditResponse:
            # BUG: Logic here make no sense. why do I return None?
            # BUG: In RedditCrawler, json.loads(res.text) sometimes caused
            #  error at the first iteration (not sure why)
            # NOTE: I dont use try-except here because this may reminds you of
            #  subtle-error
            if res.text is not None:
                res_text = res.text
                return json.loads(res_text)  # type = RedditCrawler
            # else:
            #     return None
            return res  # VALIDATE: should I return res? if not, what should
            # I return?

        def send_reddit_requests():

            after =\
                datetime.datetime.now() -\
                datetime.timedelta(days=self.max_after)
            after = int(after.timestamp())

            caches = get_response_data_with_psaw(
                max_response_cache=max_response_cache,
                kind=self.search_type,
                is_full_response=False,
                after=after,
                subreddit=self.subreddit[0],
                # filter=filter,
                # =====================
                # == variable that may cause error
                # =====================
                q=self.query[0],
                # =====================
                # == variables that are overwirtten
                # =====================
                sort=sort,
                # frequency='day',
                # aggs="created_utc",
                # metadata="true",
            )

            # caches = get_response_data_with_psaw(
            #     max_response_cache=max_response_cache,
            #     kind=self.search_type,
            #     is_full_response=False,
            #     after=after,
            #     subreddit=['askreddit'],
            #     # filter=filter,
            #     # =====================
            #     # == variable that may cause error
            #     # =====================
            #     q='OP',
            #     # =====================
            #     # == variables that are overwirtten
            #     # =====================
            #     sort='desc',
            #     # frequency='day',
            #     # aggs="created_utc",
            #     # metadata="true",
            # )

            # TODO: I still to implement so that peek first element will be
            #  used as well. Make peek compabilty with other functions.
            # if peek(caches) is None:
            #     PROGRAM_LOGGER.warn('return caches is empty.')

            total: List[Json]
            total_response_for_a_date: List[Json]
            all_full_day_response: RedditResponse
            (all_full_day_response,
            total,
             len_saved_data) = _return_response_data_from_psaw(
                caches,
                repeat,
                max_response_cache,
                None,
                None,
            )
            return all_full_day_response

            # return get_response_data_with_psaw(
            #     max_response_cache=max_response_cache,
            #     kind=self.search_type,
            #     is_full_response=False,
            #     subreddit=self.subreddit,
            #     q=self.query,
            #     sort=sort,
            # )

        # def send_reddit_requests():
        #     endpoint_url = self.get_url(running_constraints)
        #     return requests.get(endpoint_url)


        res = ensure_json(send_reddit_requests())
        check_response_keys(res)

        return res

    @my_timer
    # @signature_logger
    @deprecation.deprecated(
        deprecated_in="0.0.1",
        current_version=__version__,
        details=f"In version=={__version__}, Sending url "
                f"request and control rate limit mechanism "
                f"for pushshift is done through `psaw` "
                f"library. \n"
                f"This is so that the author does not "
                f"have to maintain those part of the code "
                f"when there are changes in pushshift.io "
                f"endpoint."
    )
    def get_responds_version_001(
            self,
            running_constraints: RedditRunningConstraints,
    ) -> RedditResponse:
        """Skipped summary.

        Prepare varaibles to be pass in (ANY) api and prepare output from (ANY)
         api.

        :type running_constraints: RedditRunningConstraints
        :param running_constraints: Dict contains keys that determines contains
         before running a crolwer

        :rtype: None or Json
        :return: respond data with appropriate respond key format
        """
        before = running_constraints["before"]
        after = running_constraints["after"]

        only_download_full_day(self.frequency, before, after)

        endpoint_url = self.get_url(running_constraints)

        def ensure_json(res) -> RedditResponse:
            # BUG: Logic here make no sense. why do I return None?
            # BUG: In RedditCrawler, json.loads(res.text) sometimes caused
            #  error at the first iteration (not sure why)
            # NOTE: I dont use try-except here because this may reminds you of
            #  subtle-error
            if res.text is not None:
                res_text = res.text
                return json.loads(res_text)  # type = RedditCrawler
            # else:
            #     return None
            return res  # VALIDATE: should I return res? if not, what should
            # I return?

        def send_reddit_requests():
            return requests.get(endpoint_url)

        # def send_reddit_requests_version_2():
        #     return

        res = ensure_json(send_reddit_requests())
        check_response_keys(res)

        return res

    @my_timer
    # @signature_logger
    def get_submission_avg_per_day(self, res: Json) -> float:
        """Skipped summary.

        Get average reddit submission per frequency given certain period of
        time.

        :type res: Json
        :param res: respond from (ANY) twitter api

        :rtype:
        :return: average submission per frequency
        """

        def check_required_key():
            assert "aggs" in res and "data" in res, ""

        check_required_key()

        created_utc = res["aggs"]["created_utc"]
        num_interval = len(created_utc)

        total = 0
        for _ind, key in enumerate(created_utc):
            total += key["doc_count"]

        avg = total / num_interval

        if self.verbose:
            # import pprint
            #
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(
            #     f" {self.current_condition_str} "
            #     f"||  avg_per_{self.frequency} given {num_interval}"
            #     f" {self.frequency}s "
            #     f"|| {avg}",
            # )

            PROGRAM_LOGGER.info(f" {self.current_condition_str} "
                                f"||  avg_per_{self.frequency} given {num_interval}"
                                f" {self.frequency}s "
                                f"|| {avg}", )

        return avg

    def run(
            self,
            before: Optional[int],
            after: int,
            max_after: int,
    ) -> Tuple[Dict[str, Dict], int, int]:
        """Skipped summary.

        crawl ALL data by running all iteration (loops) neccessary to retrieved
        all data. (this could largely depends on how selected twitter api are
        designed))

        :type before: None or int
        :param before: date in which all aata BEFORE this date should be
            retrieved

        :type after: int
        :param after: date in which all aata AFTER this date should be
            retrieved

        :param max_after: int
        :param max_after: number of (previous) frequency that will be collected

        :rtype: None or tuple of dict and int
        :return: all respond (crawled) data with appropriate respond key format
        """
        control_limit = ControlLimit()

        try:
            responds_content = self.run_once(before, after, max_after)
            total_result = responds_content["metadata"]["total_results"]
            missing_results = 1000 - total_result
            missing_results = (
                0 if np.sign(missing_results) > 0 else missing_results
            )
            if self.verbose:
                PROGRAM_LOGGER.info(
                    f" {self.current_condition_str} "
                    f"|| total_results = {total_result} "
                    f"|| missing_result = {missing_results}",
                )
            else:
                PROGRAM_LOGGER.info(f"missing_reulst = {missing_results}")
            returned_results = total_result - missing_results
        except Exception as e:
            if str(e) not in KNOWN_ERROR:
                raise NotImplementedError(
                    f"exception occur in {self.run.__name__}",
                )
            else:
                raise Warning(str(e))

        # DEPRECATED: switched to use built-in control_limit of psaw libray.
        # control_limit.control_pushshift_limit(total_number_of_request=1)

        return responds_content, returned_results, missing_results

    @my_timer
    # @signature_logger
    def run_once(
            self,
            before: Optional[int],
            after: int,
            max_after: int,
    ) -> RedditResponse:
        """
        Crawl 1 iteration (loops) neccessary to retrieved all data.

        :type before: None or int
        :param before: date in which all aata BEFORE this date should be
            retrieved

        :type after: int
        :param after: date in which all aata AFTER this date should be
            retrieved

        :param max_after: int
        :param max_after: number of (previous) frequency that will be collected

        :rtype: None or Dict
        :return: respond (crawled) data for 1 iteration with appropriate
            respond key format
        """
        try:
            running_constraints = self.prepare_running_crawler(
                before,
                after,
                max_after,
            )
            res = self.get_responds(running_constraints)
            reponds_content = self.apply_crawling_strategy(
                running_constraints,
                res,
            )
            return reponds_content
        except Exception as e:
            if str(e) not in KNOWN_ERROR:
                raise NotImplementedError(
                    f"unknown error occur in {self.run_once.__name__} ",
                )
            else:
                raise ValueError(str(e))

    def adjust_after_step(
            self,
            per_interval_average: float,
            max_responds_size: int,
    ) -> int:
        """Skipped summary.

        Dynamically adjust length of frequency to request data from api.
        (specific to reddit api (pushshift.io) behavior)

        :param per_interval_average: float
        :param per_interval_average: average number of returned data per
            interval (period) of frequency

        :param max_responds_size: int
        :param max_responds_size: maximum responds size allowed by api

        :rtype: int
        :return: length of frequency for the next iteration of run
        """
        max_responds_threshold = max_responds_size - int(
            max_responds_size * 0.40,
        )
        time_interval = int(max_responds_threshold / per_interval_average)
        time_interval = 1 if time_interval < 1 else time_interval
        return time_interval

    def get_submission_data(
            self,
            running_constraints: RedditRunningConstraints,
            res: RedditResponse,
    ) -> RedditResponse:
        """
        Get reddit (submission) data given constraint to run.

        :type running_constraints: RedditRunningConstraints
        :param running_constraints: Dict contains keys that determines contains
            before running a crolwer

        :type res: Json
        :param res: respond from (ANY) twitter api

        :rtype:  RedditResponse
        :return: respond from (ANY) reddit api
        """
        try:
            res = _get_reddit_data(res, running_constraints, self)
            # _get_reddit_aggs(res)
            res = _get_reddit_metadata(
                res,
                running_constraints,
                cast(List[str], self.aspect),
                self.query,
            )

            check_response_keys(res)
        except Exception as e:
            if str(e) != "responds are empty":
                raise NotImplementedError(
                    f"unknown error occur in "
                    f"{self.get_submission_data.__name__} ",
                )
            else:
                raise ValueError(str(e))

        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(
        #     f' {self.current_condition_str} respond data => {
        #     self.per_day_average}')  # pass in variable to be pretty printedj

        return res

    def apply_crawling_strategy(
            self,
            running_constraints: RedditRunningConstraints,
            res: RedditResponse,
    ) -> RedditResponse:
        """Skipped summary.

        Apply crawler "strategy" where a strategy is determined by selected
        collection type.

        :type running_constraints: TwitterRunningConstraints
        :param running_constraints: Dict contains keys that determines contains
            before running a crolwer

        :type res: Json
        :param res: respond from (ANY) twitter api

        :rtype: Dict
        :return: respond data with appropriate respond key format
        """
        try:
            if self.respond_type == "avg":
                raise DeprecationWarning(
                    f"no longer support {self.respond_type}",
                )

            elif self.respond_type == "data":
                return self.get_submission_data(running_constraints, res)
            else:
                raise ValueError("")
        except Exception as e:
            if str(e) != "responds are empty":
                raise NotImplementedError(
                    f"unknown error occur in "
                    f"{self.apply_crawling_strategy.__name__} ",
                )
            else:
                raise ValueError(str(e))

    def after_run(self, res: Json, after: int, max_after: int) -> Tuple:
        """Skipped summary.

        Analyze data from previous run + output neccessary data required to
        dynamically select next interval.

        :type res: Json
        :param res: respond from (ANY) twitter api

        :type after: int
        :param after: date in which all aata AFTER this date should be
            retrieved

        :param max_after: int
        :param max_after: number of (previous) frequency that will be collected

        :rtype: tuple
        :return: interval freqency for next run + average of the current
            returned data
        """
        per_interval_average: float = self.get_submission_avg_per_day(res)

        next_interval: int = self.adjust_after_step(
            per_interval_average,
            max_responds_size=1000,
        )

        # next_before, next_after, next_interval = \
        #     self._update_interval_before_after(
        #         after, max_after, next_interval)
        next_interval = (
            max_after if next_interval > max_after else next_interval
        )

        return next_interval, per_interval_average
        # return next_interval, per_interval_average, next_before, next_after

    def _get_url_endpoint_with_query_param(
            self,
            running_constraints: RedditRunningConstraints,
            after_frequency: str,
    ):
        """
        Get url with query as parameters.

        :type running_constraints: RedditRunningConstraints
        :param running_constraints: Dict contains keys that determines contains
        before running a crolwer

        :type after_frequency: str
        :param after_frequency: frequency for "after" variable

        :return:
        """
        aggs = running_constraints["aggs"]
        after = running_constraints["after"]
        size = running_constraints["size"]
        metadata = running_constraints["metadata"]
        sort = running_constraints["sort"]
        fields = running_constraints["fields"]

        all_subreddits: str = ",".join(self.collection["subreddit"])
        all_queries: str = "|".join(cast(List[str], self.collection["query"]))

        endpoint_url = (
            f"https://api.pushshift.io/reddit/"
            f"search/{self.search_type}/?"
            f"&subreddit={all_subreddits}"
            f"&q={all_queries}"
            f"&after={after}{after_frequency}"
            f"&size={size}"
            f"&metadata={metadata}"
            f"&sort={sort}"
            f"&fields={fields}"
            f"&aggs={aggs}"
            f"&frequency={self.frequency}"
        )

        return endpoint_url

    def _get_url_endpoint_without_query_param(
            self,
            running_constraints: RedditRunningConstraints,
            after_frequency: str,
    ) -> Url:
        """
        Get url without query as parameters.

        :type running_constraints: RedditRunningConstraints
        :param running_constraints: Dict contains keys that determines contains
        before running a crolwer

        :type after_frequency: str
        :param after_frequency: frequency for "after" variable

        :return:
        """
        aggs = running_constraints["aggs"]
        after = running_constraints["after"]
        size = running_constraints["size"]
        metadata = running_constraints["metadata"]
        sort = running_constraints["sort"]
        fields = running_constraints["fields"]

        all_subreddit: str = ",".join(self.collection["subreddit"])
        endpoint_url = (
            f"https://api.pushshift.io/reddit/"
            f"search/{self.search_type}/?"
            f"&subreddit={all_subreddit}"
            f"&after={after}{after_frequency}"
            f"&size={size}"
            f"&metadata={metadata}"
            f"&sort={sort}"
            f"&fields={fields}"
            f"&aggs={aggs}"
            f"&frequency={self.frequency}"
        )
        return endpoint_url

    def _update_interval_before_after(
            self,
            after: int,
            max_after_with_specified_frequency: int,
            next_interval: int,
    ) -> Tuple:
        """
        Update frequency interval for 'before' and 'after' variable.

        :type running_constraints: RedditRunningConstraints
        :param running_constraints: Dict contains keys that determines contains
        before running a crolwer

        :type after_frequency: str
        :param after_frequency: frequency for "after" variable

        :rtype: tuple
        :return: before, after, interval variable for the next run
        """
        # NOTE: this only works for day ( don't use max_after, use max_after
        #  of the same frequency
        next_before: int = (
            max_after_with_specified_frequency
            if after + 1 >= max_after_with_specified_frequency
            else after + 1
        )
        next_after: int = (
            max_after_with_specified_frequency
            if next_before + next_interval
               >= max_after_with_specified_frequency
            else next_before + next_interval
        )  # type: ignore

        # next_interval: int = next_before - next_after
        next_interval_: int = next_after - next_before

        return next_before, next_after, next_interval_


class RedditCrawlerCondition(TypedDict):
    """Skipped."""

    crawler_class: Type[RedditCrawler]
    collection_class: SubredditCollection
    initial_interval: int
    request_timestamp: datetime.datetime
    respond_type: str
    search_type: str
    frequency: Frequency
    verbose: bool
    # aspect: Optional[str]
    max_after: int


def run_reddit_crawler(
        reddit_crawler_condition: RedditCrawlerCondition,
) -> Tuple[int, int]:
    """Skipped summay.


    :type reddit_crawler_condition: RedditCrawlerCondition
    :param reddit_crawler_condition: shared conditions (constraints) not
        specific to any given crawler

    :return: list of int
    :return: total number of returned responds data + total missing respond
        data
    """
    crawler_class: Type[RedditCrawler] = reddit_crawler_condition[
        "crawler_class"
    ]
    subreddits_collection_class = reddit_crawler_condition["collection_class"]
    initial_interval = reddit_crawler_condition["initial_interval"]
    request_timestamp = reddit_crawler_condition[  # noqa: F841
        "request_timestamp"
    ]
    respond_type = reddit_crawler_condition["respond_type"]
    search_type = reddit_crawler_condition["search_type"]
    frequency = reddit_crawler_condition["frequency"]  # noqa: F841
    verbose = reddit_crawler_condition["verbose"]
    max_after = reddit_crawler_condition["max_after"]
    aspect = reddit_crawler_condition["collection_class"]["collection"][
        "aspect"
    ]

    after = initial_interval
    before = None
    # next_interval = None
    # frequency = frequency  # , 'second', 'minute', 'day'
    assert after <= max_after, "after have to be less than max_after"
    # saved_path = None

    max_after_epoch_datetime = _get_epoch_datetime_subtract_timedelta(
        datetime.datetime.now(),
        "day",
        max_after,
    )
    max_after_epoch_datetime_date = max_after_epoch_datetime.date()

    # OPTIMIZE: the paragraph of code below is badly implemented. Please
    #  take time to refactor if I will ever use it again. Keep in mind it
    #  may have few unintended side effect. Be sure to constantly test when
    #  refactoring.
    #
    # DEPRECATED: the paragraph of code is outdated because I use
    #  psaw library to deal with returning data in batch and control limit.
    def _select_optimize_frequency(
            before: Optional[int] = None,
            after: int = 100,
    ) -> Tuple[int, Frequency]:
        PROGRAM_LOGGER.info(
            "selecting optimized frequency length among: day, hour, minute,"
            " second ",
        )
        # sorted_frequency_rank = ["day", "hour", "minute", "second"]
        sorted_frequency_rank: List[Frequency] = ["day",
                                                  "hour",
                                                  "minute",
                                                  "second"]

        def _count_num_missing_value(res: Json) -> int:
            num_missing_val = res["metadata"]["total_results"] - len(
                res["data"],
            )
            return num_missing_val

        condition = True

        while condition:
            frequency: Frequency = sorted_frequency_rank[0]

            reddit_crawler = crawler_class(
                subreddits_collection_class=subreddits_collection_class,
                respond_type=respond_type,
                search_type=search_type,
                frequency=frequency,
                verbose=verbose,
                aspect=aspect,
                max_after=max_after,
            )

            responds_content, _, _ = reddit_crawler.run(
                before,
                after,
                max_after,
            )

            if len(responds_content["data"]) > 0:
                if (
                        _count_num_missing_value(responds_content) > 0
                ):  # if next_interval
                    # (predicted_interval) still have too many respon
                    next_interval, per_day_average = reddit_crawler.after_run(
                        responds_content,
                        after,
                        max_after,
                    )

                    if next_interval == 1 and per_day_average > 1000:  # if
                        # there are too many responds per day
                        sorted_frequency_rank = sorted_frequency_rank[1:]

                        PROGRAM_LOGGER.info(
                            f" || adjust frequency from "
                            f'{reddit_crawler_condition["frequency"]} to'
                            f" {sorted_frequency_rank[0]} \n",
                        )

                        reddit_crawler_condition[
                            "frequency"
                        ] = sorted_frequency_rank[0]
                    else:
                        # after = max_after if next_interval > max_after
                        # else next_interval
                        after = next_interval  # assigned predicted interval

                        assert after <= max_after, ""

                        PROGRAM_LOGGER.info(
                            f" Given frequency = {frequency} "
                            f"|| adjust initial_interval(after) "
                            f"from "
                            f'{reddit_crawler_condition["initial_interval"]} '
                            f"to {after} \n",
                        )

                        reddit_crawler_condition["initial_interval"] = after

                    return after, frequency
                else:
                    after_timestamp_utc = (
                        _get_epoch_datetime_subtract_timedelta(
                            datetime.datetime.now(),
                            frequency,
                            after,
                        )
                    )

                    time_diff = datetime.datetime.now() - after_timestamp_utc

                    after = _convert_timedelta_to_specified_frequency(
                        time_diff,
                        frequency,
                    )

                    reddit_crawler_condition["initial_interval"] = after
                    reddit_crawler_condition["frequency"] = frequency
                    PROGRAM_LOGGER.info(
                        f"Given frequency = {frequency} "
                        f"|| after is set to "
                        f"{reddit_crawler_condition['initial_interval']} \n",
                    )

                    return after, frequency
            else:
                if after >= max_after:
                    raise ValueError("responses are empty")
                else:
                    raise NotImplementedError
        else:
            raise NotImplementedError("This line shouldn't be reached. I"
                                      "added this line to bypass mypy false "
                                      "positive.")

    # VALIDATE: I validated it, but it may missed something, so this is left
    #  here for future debugging
    after, frequency = _select_optimize_frequency(after=max_after)
    assert after <= max_after, ""

    total_returned_data = 0
    total_missing_data = 0

    # request_timestamp_str = get_full_datetime_str(request_timestamp)

    max_after_delta = _get_epoch_datetime_subtract_timedelta(
        datetime.datetime.now(),
        "day",
        max_after,
    )
    time_diff = datetime.datetime.now() - max_after_delta

    max_after_with_specified_frequency = (
        _convert_timedelta_to_specified_frequency(time_diff, frequency)
    )

    terminal_condition = True
    while terminal_condition:

        reddit_crawler = crawler_class(
            subreddits_collection_class=subreddits_collection_class,
            respond_type=respond_type,
            search_type=search_type,
            frequency=frequency,
            verbose=verbose,
            aspect=aspect,
            max_after=max_after,
        )

        PROGRAM_LOGGER.info(
            f'aspect = {aspect}\n'
            f'|| collection_name={subreddits_collection_class["collection"]}\n'
            f'|| search_type = {search_type}\n'
            f'|| respond_type = {respond_type}\n'
            f'|| frequency = {frequency}\n'
            f'|| {after} <= x < {before}\n')

        try:
            (
                responds_content,
                num_returned_data,
                num_missing_data,
            ) = reddit_crawler.run(before, after, max_after)

            total_returned_data += num_returned_data
            total_missing_data += num_missing_data

            next_interval, per_day_averagee = reddit_crawler.after_run(
                responds_content,
                after,
                max_after,
            )

            saved_file = get_saved_file_path(
                reddit_crawler.time_since,
                reddit_crawler.time_until,
                path_name=BASE_DIR / f"Outputs/Data/"  # noqa: E251
                                     f"{reddit_crawler.crawler_name}/"
                                     f"{reddit_crawler.aspect}/"
                                     f"{reddit_crawler.collection_name}/"
                                     f"{reddit_crawler.search_type}/"
                                     f"{reddit_crawler.respond_type}",
            )
            save_to_file(responds_content, saved_file)

        except Exception as e:

            if str(e) not in KNOWN_ERROR:
                raise NotImplementedError(
                    f"unknown error occur in {run_reddit_crawler.__name__} ",
                )
            else:
                PROGRAM_LOGGER.error("responds are empty")
                next_interval = after  # reintialize next-interval to be last
                # calculated per_day_average

        # =====================
        # == update parameters for the next iteration.
        # =====================

        if reddit_crawler.timestamp_utc.date() < max_after_epoch_datetime_date:
            reddit_crawler.timestamp_utc = max_after_epoch_datetime

        after = (
            _ensure_datetime_for_specified_frequency_not_consider_max_after(
                reddit_crawler.timestamp_utc,
                max_after_epoch_datetime,
                frequency,
                after,
            )
        )
        # print(reddit_crawler.timestamp_utc)
        # print(after)
        # exit()

        if after == max_after_with_specified_frequency:
            terminal_condition = False

        reddit_crawler.timestamp_utc = _get_epoch_datetime_subtract_timedelta(
            reddit_crawler.timestamp_utc,
            reddit_crawler.frequency,
            next_interval,
        )

        (
            before,
            after,
            next_interval,
        ) = reddit_crawler._update_interval_before_after(
            after,
            max_after_with_specified_frequency,
            next_interval,
        )

        assert after <= max_after_with_specified_frequency, ""

    PROGRAM_LOGGER.info(
        f"|| total returned data = {total_returned_data} "
        f"|| total_missing_data = {total_missing_data}",
    )
    PROGRAM_LOGGER.info(" >>>> finished crawling data <<<< \n")
    return total_returned_data, total_missing_data


# NOTE: I am not sure what casued missing data when request urls are exactly
#     the same prepared varaibles, check conditions, run crawlers and saved
#     respond data.
@deprecation.deprecated(deprecated_in="0.0.1",
                        current_version=__version__,
                        details=f"In version=={__version__}, Sending url "
                                f"request and control rate limit mechanism "
                                f"for pushshift is done through `psaw` "
                                f"library. \n"
                                f"This is so that the author does not "
                                f"have to maintain those part of the code "
                                f"when there are changes in pushshift.io "
                                f"endpoint.")
def run_reddit_crawler_version_001(
        reddit_crawler_condition: RedditCrawlerCondition,
) -> Tuple[int, int]:
    """Skipped summay.


    :type reddit_crawler_condition: RedditCrawlerCondition
    :param reddit_crawler_condition: shared conditions (constraints) not
        specific to any given crawler

    :return: list of int
    :return: total number of returned responds data + total missing respond
        data
    """
    crawler_class: Type[RedditCrawler] = reddit_crawler_condition[
        "crawler_class"
    ]
    subreddits_collection_class = reddit_crawler_condition["collection_class"]
    initial_interval = reddit_crawler_condition["initial_interval"]
    request_timestamp = reddit_crawler_condition[  # noqa: F841
        "request_timestamp"
    ]
    respond_type = reddit_crawler_condition["respond_type"]
    search_type = reddit_crawler_condition["search_type"]
    frequency = reddit_crawler_condition["frequency"]  # noqa: F841
    verbose = reddit_crawler_condition["verbose"]
    max_after = reddit_crawler_condition["max_after"]
    aspect = reddit_crawler_condition["collection_class"]["collection"][
        "aspect"
    ]

    after = initial_interval
    before = None
    # next_interval = None
    # frequency = frequency  # , 'second', 'minute', 'day'
    assert after <= max_after, "after have to be less than max_after"
    # saved_path = None

    max_after_epoch_datetime = _get_epoch_datetime_subtract_timedelta(
        datetime.datetime.now(),
        "day",
        max_after,
    )
    max_after_epoch_datetime_date = max_after_epoch_datetime.date()

    # OPTIMIZE: the paragraph of code below is badly implemented. Please
    #  take time to refactor if I will ever use it again. Keep in mind it
    #  may have few unintended side effect. Be sure to constantly test when
    #  refactoring.
    #
    # DEPRECATED: the paragraph of code is outdated because I use
    #  psaw library to deal with returning data in batch and control limit.
    def _select_optimize_frequency(
            before: Optional[int] = None,
            after: int = 100,
    ) -> Tuple[int, Frequency]:
        PROGRAM_LOGGER.info(
            "selecting optimized frequency length among: day, hour, minute,"
            " second ",
        )
        # sorted_frequency_rank = ["day", "hour", "minute", "second"]
        sorted_frequency_rank: List[Frequency] = ["day",
                                                  "hour",
                                                  "minute",
                                                  "second"]

        def _count_num_missing_value(res: Json) -> int:
            num_missing_val = res["metadata"]["total_results"] - len(
                res["data"],
            )
            return num_missing_val

        condition = True

        while condition:
            frequency: Frequency = sorted_frequency_rank[0]

            reddit_crawler = crawler_class(
                subreddits_collection_class=subreddits_collection_class,
                respond_type=respond_type,
                search_type=search_type,
                frequency=frequency,
                verbose=verbose,
                aspect=aspect,
                max_after=max_after,
            )

            responds_content, _, _ = reddit_crawler.run(
                before,
                after,
                max_after,
            )

            if len(responds_content["data"]) > 0:
                if (
                        _count_num_missing_value(responds_content) > 0
                ):  # if next_interval
                    # (predicted_interval) still have too many respon
                    next_interval, per_day_average = reddit_crawler.after_run(
                        responds_content,
                        after,
                        max_after,
                    )

                    if next_interval == 1 and per_day_average > 1000:  # if
                        # there are too many responds per day
                        sorted_frequency_rank = sorted_frequency_rank[1:]

                        PROGRAM_LOGGER.info(
                            f" || adjust frequency from "
                            f'{reddit_crawler_condition["frequency"]} to'
                            f" {sorted_frequency_rank[0]} \n",
                        )

                        reddit_crawler_condition[
                            "frequency"
                        ] = sorted_frequency_rank[0]
                    else:
                        # after = max_after if next_interval > max_after
                        # else next_interval
                        after = next_interval  # assigned predicted interval

                        assert after <= max_after, ""

                        PROGRAM_LOGGER.info(
                            f" Given frequency = {frequency} "
                            f"|| adjust initial_interval(after) "
                            f"from "
                            f'{reddit_crawler_condition["initial_interval"]} '
                            f"to {after} \n",
                        )

                        reddit_crawler_condition["initial_interval"] = after

                    return after, frequency
                else:
                    after_timestamp_utc = (
                        _get_epoch_datetime_subtract_timedelta(
                            datetime.datetime.now(),
                            frequency,
                            after,
                        )
                    )

                    time_diff = datetime.datetime.now() - after_timestamp_utc

                    after = _convert_timedelta_to_specified_frequency(
                        time_diff,
                        frequency,
                    )

                    reddit_crawler_condition["initial_interval"] = after
                    reddit_crawler_condition["frequency"] = frequency
                    PROGRAM_LOGGER.info(
                        f"Given frequency = {frequency} "
                        f"|| after is set to "
                        f"{reddit_crawler_condition['initial_interval']} \n",
                    )

                    return after, frequency
            else:
                if after >= max_after:
                    raise ValueError("responses are empty")
                else:
                    raise NotImplementedError
        else:
            raise NotImplementedError("This line shouldn't be reached. I"
                                      "added this line to bypass mypy false "
                                      "positive.")

    # VALIDATE: I validated it, but it may missed something, so this is left
    #  here for future debugging
    # after, frequency = _select_optimize_frequency(after=max_after)
    assert after <= max_after, ""

    total_returned_data = 0
    total_missing_data = 0

    # request_timestamp_str = get_full_datetime_str(request_timestamp)

    max_after_delta = _get_epoch_datetime_subtract_timedelta(
        datetime.datetime.now(),
        "day",
        max_after,
    )
    time_diff = datetime.datetime.now() - max_after_delta

    max_after_with_specified_frequency = (
        _convert_timedelta_to_specified_frequency(time_diff, frequency)
    )

    terminal_condition = True
    while terminal_condition:

        reddit_crawler = crawler_class(
            subreddits_collection_class=subreddits_collection_class,
            respond_type=respond_type,
            search_type=search_type,
            frequency=frequency,
            verbose=verbose,
            aspect=aspect,
            max_after=max_after,
        )

        PROGRAM_LOGGER.info(
            f'aspect = {aspect}\n'
            f'|| collection_name={subreddits_collection_class["collection"]}\n'
            f'|| search_type = {search_type}\n'
            f'|| respond_type = {respond_type}\n'
            f'|| frequency = {frequency}\n'
            f'|| {after} <= x < {before}\n')

        try:
            (
                responds_content,
                num_returned_data,
                num_missing_data,
            ) = reddit_crawler.run(before, after, max_after)

            total_returned_data += num_returned_data
            total_missing_data += num_missing_data

            next_interval, per_day_averagee = reddit_crawler.after_run(
                responds_content,
                after,
                max_after,
            )

            saved_file = get_saved_file_path(
                reddit_crawler.time_since,
                reddit_crawler.time_until,
                path_name=BASE_DIR / f"Outputs/Data/"  # noqa: E251
                                     f"{reddit_crawler.crawler_name}/"
                                     f"{reddit_crawler.aspect}/"
                                     f"{reddit_crawler.collection_name}/"
                                     f"{reddit_crawler.search_type}/"
                                     f"{reddit_crawler.respond_type}",
            )
            save_to_file(responds_content, saved_file)

        except Exception as e:

            if str(e) not in KNOWN_ERROR:
                raise NotImplementedError(
                    f"unknown error occur in {run_reddit_crawler.__name__} ",
                )
            else:
                PROGRAM_LOGGER.error("responds are empty")
                next_interval = after  # reintialize next-interval to be last
                # calculated per_day_average

        # =====================
        # == update parameters for the next iteration.
        # =====================

        if reddit_crawler.timestamp_utc.date() < max_after_epoch_datetime_date:
            reddit_crawler.timestamp_utc = max_after_epoch_datetime

        after = (
            _ensure_datetime_for_specified_frequency_not_consider_max_after(
                reddit_crawler.timestamp_utc,
                max_after_epoch_datetime,
                frequency,
                after,
            )
        )
        print(reddit_crawler.timestamp_utc)
        print(after)
        exit()

        if after == max_after_with_specified_frequency:
            terminal_condition = False

        reddit_crawler.timestamp_utc = _get_epoch_datetime_subtract_timedelta(
            reddit_crawler.timestamp_utc,
            reddit_crawler.frequency,
            next_interval,
        )

        (
            before,
            after,
            next_interval,
        ) = reddit_crawler._update_interval_before_after(
            after,
            max_after_with_specified_frequency,
            next_interval,
        )

        assert after <= max_after_with_specified_frequency, ""

    PROGRAM_LOGGER.info(
        f"|| total returned data = {total_returned_data} "
        f"|| total_missing_data = {total_missing_data}",
    )
    PROGRAM_LOGGER.info(" >>>> finished crawling data <<<< \n")
    return total_returned_data, total_missing_data


# =====================
# ==Reddit Test
# =====================
# FIXME: this function should be method of TwitterCrawler class.
#     (Is there any reason not to?)
def _get_reddit_metadata(
        res: RedditResponse,
        running_constraints: RedditRunningConstraints,
        aspect: Tags,
        query: Query,
) -> RedditResponse:
    """Prepare 'metadata' key in respond data to have an appropriate format.

    :type respond_type: str
    :param respond_type: desired respond type by crawler

    :type running_constraints: TwitterRunningConstraints
    :param running_constraints: Dict contains keys that determines contains
    before running a crolwer

    :type crawler_instance: TwitterCrawler
    :param crawler_instance: twitter crawler class

    :type aspect: Tags
    :param aspect: any specified aspect

    :type query: Query
    :param query: list of words assigned for a selected aspect

    :rtype: Json
    :return: respond data with appropriate 'metadata' key format
    """
    metadata: RedditMetadata = {}
    metadata["running_constraints"] = running_constraints


    # filter out fields that we don't want
    for key in REDDIT_META_DATA_KEYS:
        metadata[key] = res["metadata"][key]  # type: ignore

    res["metadata"] = metadata

    # add fields that are not provided by pushshift api
    res["metadata"]["aspect"] = aspect
    res["metadata"]["query"] = query

    return res


# FIXME: this function should be method of TwitterCrawler class. (Is there
#     any reason not to?)
@my_timer
def _get_reddit_data(
        res: RedditResponse,
        running_constraints: RedditRunningConstraints,
        crawler_class: RedditCrawler,
        # add_sentiment_key=True,
        # add_sentiment_key=False,
) -> RedditResponse:
    """Prepare 'data' key in respond data to have an appropriate format.

    :type respond_type: str
    :param respond_type: desired respond type by crawler

    :type running_constraints: TwitterRunningConstraints
    :param running_constraints: Dict contains keys that determines contains
    before running a crolwer

    :type crawler_instance: TwitterCrawler
    :param crawler_instance: twitter crawler class

    :rtype: Json
    :return: respond data with appropriate 'data' key format
    """

    def _check_responds_consistency():
        if len(res["data"]) > 0:
            for i in range(len(res["data"])):
                check_that_all_selected_fields_are_returns(
                    running_constraints,
                    res,
                    i,
                    crawler_class.current_condition_str,
                    crawler_class.verbose,
                )
        else:
            # print('response are empty')
            raise Warning("responds are empty")

    # @my_timer
    def _get_sentiment(x,
                       # _add_sentiment_key: bool
                       ) -> float:
        """Skipped.


        BUG: _add_sentiment_key cause error when update and sentiment key
          has value = None

        :param x:
        :return:
        """

        # if not _add_sentiment_key:
        # if True:
        #     return None

        text: Optional[str]

        if crawler_class.search_type == "comment":
            text = x["body"]
        elif crawler_class.search_type == "submission":
            text = x["title"]
        else:
            raise NotImplementedError

        if text is None:
            return 0.0
        else:
            sentiment_polarity = get_sentiment(text)
            return sentiment_polarity

    try:
        _check_responds_consistency()
    except Exception as e:
        if str(e) != "responds are empty":
            raise NotImplementedError(
                f"unknown error occur in {_get_reddit_data.__name__} ",
            )
        else:
            raise ValueError(str(e))

    all_data_with_sentiment = []
    for data in tqdm(res["data"]):
        data_with_sentiment = data
        sentiment_value = _get_sentiment(
            data,
            # add_sentiment_key,
        )
        if sentiment_value is not None:
            data_with_sentiment["sentiment"] = sentiment_value
        all_data_with_sentiment.append(data_with_sentiment)

    res["data"] = all_data_with_sentiment

    return res


def _get_reddit_aggs(res: Json) -> None:
    """Skipped."""
    raise NotImplementedError


if __name__ == '__main__':
    print('hi')
