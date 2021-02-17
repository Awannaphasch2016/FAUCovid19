import datetime
import datetime as dt
# import json
import inspect
import json
import logging
import os
import pathlib
import pickle
from itertools import product
from os import walk
from typing import Dict
from typing import Generator
from typing import List
from typing import Tuple
from typing import Union

import pytest

from global_parameters import ALL_ASPECTS
from global_parameters import ALL_CRAWLERS
from global_parameters import ALL_REDDIT_COLLECTION_NAMES
from global_parameters import BASE_DIR
from global_parameters import MAX_AFTER
from global_parameters import REDDIT_SORT
from src.Sources.Preparations.Data import get_crawler_running_conditions
from src.Sources.Preparations.Data import select_crawler_condition
from src.Sources.Preparations.Data.reddit_crawler import ALL_PSAW_SEARCH_KINDS
from src.Sources.Preparations.Data.reddit_crawler import _return_response_data_from_psaw
from src.Sources.Preparations.Data.reddit_crawler import \
    get_response_data_with_psaw
from src.Sources.Preparations.Data.reddit_crawler import psaw_api
from src.Utilities import Json
from src.Utilities import RedditResponse
from src.Utilities import Sort
from src.Utilities import save_to_file
from src.Utilities.CheckConditions.check_conditions import \
    check_running_conditions

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


@pytest.fixture
def start_epoch() -> int:
    # start_epoch = int(dt.datetime(2020, 9, 5).timestamp())
    start_epoch = int(dt.datetime(2020, 10, 10).timestamp())
    return start_epoch




def _are_all_reponse_data_returned(response: List[Json],
                                   max_response_cache: int,
                                   repeat: int) -> bool:
    # NOTE: that it is possible that len(total) < max_response_cache.
    #   This happen when number of returned data < max_response_cache.
    if len(response) > 0:
        # print(f"len(response) = {len(response)}")
        # print(f"max_response_cache= = {max_response_cache}")
        # print(f"repeat = {repeat}")
        return len(response) <= max_response_cache * repeat

    return True




class TestPSAW:

    def setup_class(self):
        def _get_responds_directly_from_url(kind: str) -> Json:
            # BUG: sometimes, response return 502 error. (pushfhit server
            #  has too many requests. This is usually a temporary problem.),
            #  with that being that, How do I test this when I don't know
            #  when reddit will be down and how long it will be down for.
            while True:
                url = f'https://api.pushshift.io/reddit/search/{kind}' \
                      '/?&subreddit=Corona&size=5'
                import requests
                response = requests.get(url)
                LOGGER.debug(f'url = {url}')
                LOGGER.debug(f'response_status_code = response.status_code')
                if response.status_code == 200:
                    return json.loads(response.text)
                elif response.status_code == 502:
                    pass
                else:
                    raise NotImplementedError(response.status_code)

        self.direct_submission_responds_from_pushshift_endpoint = \
            _get_responds_directly_from_url(ALL_PSAW_SEARCH_KINDS[0])

        self.direct_comment_responds_from_pushshift_endpoint = \
            _get_responds_directly_from_url(ALL_PSAW_SEARCH_KINDS[1])

    def _are_all_response_keys_returned_from_pushshift_endpoint(
            self,
            response: List[Json],
            kind: str,
    ) -> bool:
        LOGGER.info(
            f"{inspect.currentframe().f_code.co_name}"
            f" is running ..."  # type: ignore
        )

        # NOTE: I am sure in which scenario these keys are returned, but it
        #  is clear that response does not always have all keys.

        if kind == ALL_PSAW_SEARCH_KINDS[0]:

            unknown_keys_from_psaw = ("suggested_sort",)
            garantee_pushshift_keys = ('post_hint',
                                       'preview',
                                       'thumbnail_height',
                                       'thumbnail_width',
                                       'url_overridden_by_dest',
                                       'link_flair_template_id',
                                       'link_flair_text',
                                       'removed_by_category',
                                       'author_flair_background_color',
                                       'url',
                                       'parent_id',
                                       'is_video',
                                       'is_submitter',
                                       'subreddit_subscribers',
                                       'is_crosspostable',
                                       'parent_whitelist_status',
                                       'pinned',
                                       'whitelist_status',
                                       'is_robot_indexable',
                                       'media_only',
                                       'pwls',
                                       'top_awarded_type',
                                       'spoiler',
                                       'full_link',
                                       'num_crossposts',
                                       'associated_award',
                                       'link_flair_type',
                                       'collapsed_because_crowd_control',
                                       'author_flair_template_id',
                                       'num_comments',
                                       'distinguished',
                                       'is_reddit_media_domain',
                                       'is_meta',
                                       'can_mod_post',
                                       'over_18',
                                       'selftext',
                                       'subreddit_type',
                                       'link_id',
                                       'domain',
                                       'is_self',
                                       'link_flair_richtext',
                                       'wls',
                                       'upvote_ratio',
                                       'author_flair_text_color',
                                       'body',
                                       'comment_type',
                                       'contest_mode',
                                       'allow_live_comments',
                                       'is_original_content',
                                       'link_flair_text_color',
                                       'title',
                                       'thumbnail',
                                       'link_flair_background_color',
                                       'crosspost_parent',
                                       'crosspost_parent_list',
                                       'is_gallery'
                                       )

        elif kind == ALL_PSAW_SEARCH_KINDS[1]:

            unknown_keys_from_psaw = ("distinguished",)
            garantee_pushshift_keys = ('author_flair_type',
                                       'distinguished',
                                       'author_fullname',
                                       'author_flair_richtext',
                                       'author_patreon_flair',
                                       'author_premium'
                                       )

        if len(response) > 0:
            # print("inside")

            if kind == ALL_PSAW_SEARCH_KINDS[0]:
                all_pushshift_keys = \
                    tuple(
                        self.direct_submission_responds_from_pushshift_endpoint \
                            ['data'][0].keys()
                    )
            elif kind == ALL_PSAW_SEARCH_KINDS[1]:
                all_pushshift_keys = \
                    tuple(
                        self.direct_comment_responds_from_pushshift_endpoint \
                            ['data'][0].keys()
                    )

            # all_pushshift_keys = \
            #     tuple(
            #         self.direct_submission_responds_from_pushshift_endpoint \
            #             ['data'][0].keys())

            returned_response_keys = tuple(response[0].keys())

            all_pushshift_keys1 = \
                tuple(self.direct_comment_responds_from_pushshift_endpoint[
                          'data'][
                          1] \
                      .keys())
            returned_response_keys1 = tuple(response[1].keys())
            all_pushshift_keys2 = \
                tuple(self.direct_comment_responds_from_pushshift_endpoint[
                          'data'][
                          2] \
                      .keys())
            returned_response_keys2 = tuple(response[2].keys())
            all_pushshift_keys3 = \
                tuple(self.direct_comment_responds_from_pushshift_endpoint[
                          'data'][
                          3] \
                      .keys())
            returned_response_keys3 = tuple(response[2].keys())
            all_pushshift_keys4 = \
                tuple(self.direct_comment_responds_from_pushshift_endpoint[
                          'data'][
                          4] \
                      .keys())
            returned_response_keys4 = tuple(response[3].keys())

            all_pushshift_keys += \
                unknown_keys_from_psaw + garantee_pushshift_keys
            returned_response_keys += \
                unknown_keys_from_psaw + garantee_pushshift_keys

            all_pushshift_keys = set(all_pushshift_keys)
            returned_response_keys = set(returned_response_keys)

            all_pushshift_keys1 = set(all_pushshift_keys1)
            returned_response_keys1 = set(returned_response_keys1)
            all_pushshift_keys2 = set(all_pushshift_keys2)
            returned_response_keys2 = set(returned_response_keys2)
            all_pushshift_keys3 = set(all_pushshift_keys3)
            returned_response_keys3 = set(returned_response_keys3)
            all_pushshift_keys4 = set(all_pushshift_keys4)
            returned_response_keys4 = set(returned_response_keys4)

            # print(all_pushshift_keys. \
            #       symmetric_difference(returned_response_keys))

            return len(all_pushshift_keys. \
                       symmetric_difference(returned_response_keys)) == 0

        return True

    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    @pytest.mark.parametrize("kind",
                             [
                                 i for i in ALL_PSAW_SEARCH_KINDS

                                 # "submission",
                             ]
                             )
    def test_psaw_original(self, start_epoch, kind):
        """Test psaw.search_submission basic funcationality.


        Test_psaw_original test the following.
         1. number of returned amount is correct (no missing response)
         2. number of response['data'] keys are all returned
        """
        LOGGER.info(f"{inspect.currentframe().f_code.co_name} is running ...")

        subreddit = ['corona']
        sort: Sort = REDDIT_SORT[1]
        query = 'covid'

        # NOTE: max_response_cache needs to be more than 100 because
        #  psaw.search_comment yield for 100 per iteration.

        max_response_cache = 101
        repeat = 3

        # max_response_cache = 5
        # repeat = 3

        caches = get_response_data_with_psaw(
            max_response_cache=max_response_cache,
            kind=kind,
            is_full_response=False,
            subreddit=subreddit,
            q=query,
            sort=sort,
        )

        total: List[Json]
        total_response_for_a_date: List[Json]
        all_full_day_response: RedditResponse

        (all_full_day_response,
         total,
         len_saved_data) =\
            _return_response_data_from_psaw(
            caches,
            repeat,
            max_response_cache,
            None,
            None,
        )

        if not _are_all_reponse_data_returned(total, max_response_cache,
                                              repeat):
            raise ValueError

        # if not self._are_all_response_keys_returned_from_pushshift_endpoint(
        #         total,
        #         kind,
        # ):
        #     raise ValueError

        LOGGER.debug('complete')

    @pytest.mark.parametrize("kind",
                             [
                                 "submission"
                             ]
                             )
    def test_all_day_from_response_data_are_saved(self, start_epoch, kind):
        """Test psaw.search_submission basic funcationality.


        Test_psaw_original test the following.
         1. number of returned amount is correct (no missing response)
         2. number of response['data'] keys are all returned
        """
        LOGGER.info(f"{inspect.currentframe().f_code.co_name} is running...")

        subreddit = ['corona']
        sort: Sort = REDDIT_SORT[1]
        query_str = 'covid'
        LOGGER.debug(f'query_str = {query_str}')

        max_response_cache = 101
        repeat = 1

        save_file \
            = "saved_pushshift_response_{}.pickle"
        save_path = pathlib.Path(BASE_DIR) \
                    / r"Examples\Libraries\PSAWLibrary\SaveSampleOutput"

        def _delete_all_saved_full_day_file(_save_path: pathlib.Path):

            filelist = [f for f in os.listdir(str(_save_path))]
            for f in filelist:
                os.remove(os.path.join(str(_save_path), f))

        _delete_all_saved_full_day_file(save_path)

        caches = get_response_data_with_psaw(
            max_response_cache=max_response_cache,
            kind=kind,
            is_full_response=False,
            subreddit=subreddit,
            q=query_str,
            sort=sort,
        )

        total: List[Json]
        total_response_for_a_date: List[Json]
        all_full_day_response_data: List[Json]
        (all_full_day_response_data, total, len_saved_data) = _return_response_data_from_psaw(
            caches,
            repeat,
            max_response_cache,
            save_path,
            save_file,
        )

        if not _are_all_reponse_data_returned(total, max_response_cache,
                                              repeat):
            raise ValueError

        if not self._are_all_response_keys_returned_from_pushshift_endpoint(
                total,
                kind,
        ):
            raise ValueError

        def _get_data_from_all_saved_full_day_file(
                _save_path: pathlib.Path) -> List[Json]:

            all_full_day_data: List[Json] = []
            for (dirpath, dirnames, filenames) in walk(_save_path):
                for file in filenames:
                    full_day_data = \
                        pickle.load(open(str(_save_path / file), "rb"))
                    all_full_day_data.extend(full_day_data)

            return all_full_day_data

        all_full_day_data: List[Json] = \
            _get_data_from_all_saved_full_day_file(save_path)

        assert len_saved_data == len(all_full_day_data)

        LOGGER.info('complete')

    @pytest.mark.parametrize("kind,aspect,collection_name",
                             [

                                 # (i, j, k) for i, j, k in
                                 # product(ALL_PSAW_SEARCH_KINDS,
                                 #         ALL_ASPECTS,
                                 #         ALL_REDDIT_COLLECTION_NAMES[:-1]
                                 #         )

                                 # ("submission", "work_from_home"),
                                 # ("submission", "corona"),
                                 # ("comment", "corona"),
                                 ("submission", "corona", "corona_general"),
                                 # ("submission", "corona", "corona_regions"),

                             ]
                             )
    def test_psaw_search_with_one_query(self,
                                        start_epoch,
                                        kind,
                                        aspect,
                                        collection_name,
                                        ):
        """Skipped."""
        LOGGER.info(f"{inspect.currentframe().f_code.co_name} is running ...")

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

            if collection_name ==\
                    crawler_condition['collection_class']['name']:
                break

        sort: Sort = running_conditions['sort']
        subreddit: List[str] \
            = crawler_condition['collection_class']['collection']['subreddit']
        aspect: List[str] \
            = crawler_condition['collection_class']['collection']['aspect']
        query: List[str] \
            = crawler_condition['collection_class']['collection']['query']
        query_str = query[0]

        assert aspect in ALL_ASPECTS

        # =====================
        # == set test parameters and execucte test
        # =====================

        max_response_cache = 5
        repeat = 3
        # max_response_cache = 50
        # repeat = 100

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

        total: List[Json]
        total_response_for_a_date: List[Json]
        all_full_day_response_data: List[Json]
        (all_full_day_response_data, total, len_saved_data) = _return_response_data_from_psaw(
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

        if not self._are_all_response_keys_returned_from_pushshift_endpoint(
                total,
                kind,
        ):
            raise ValueError

        LOGGER.info('complete')

    @pytest.mark.parametrize("kind,aspect",
                             [

                                 # (i, j) for i, j in
                                 # product(ALL_PSAW_SEARCH_KINDS,
                                 #         ALL_ASPECTS)

                                 # ("submission", "work_from_home"),
                                 ("comment", "work_from_home")

                             ])
    def test_psaw_search_with_multiple_query(self,
                                             start_epoch,
                                             kind,
                                             aspect):
        """Skipped."""

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

        for query_num in list(range(len(query))):

            query_str: str = '|'.join(query[:query_num + 1])

            max_response_cache = 1000
            repeat = 1
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

            if not self._are_all_response_keys_returned_from_pushshift_endpoint(
                    total,
                    kind,
            ):
                raise ValueError

            assert \
                previous_response_num <= len(total), \
                "The last added query cause number of response to reduces " \
                "which is not logically correct due to potentially bug from" \
                " pushshift.io api"
            previous_response_num = len(total)

        LOGGER.info('complete')


if __name__ == '__main__':
    pass

    test_psaw = TestPSAW()

    # start_epoch = int(dt.datetime(2020, 9, 5).timestamp())
    # test_psaw.test_psaw_original(
    #     # int(dt.datetime(2020, 10, 7).timestamp()),
    #     # int(dt.datetime(2020, 10, 10).timestamp()),
    #     int(dt.datetime(2020, 9, 5).timestamp()),  # start_epoch
    #     "submission",
    # )

    # test_psaw.test_all_day_from_response_data_are_saved(
    #     # int(dt.datetime(2020, 10, 7).timestamp()),
    #     int(dt.datetime(2020, 10, 10).timestamp()),
    #     "submission",
    # )

    # test_psaw.test_psaw_search_with_one_query_with_corona_general_collection(
    #     # int(dt.datetime(2020, 10, 7).timestamp()),
    #     # int(dt.datetime(2020, 10, 10).timestamp()),
    #     int(dt.datetime(2020, 9, 5).timestamp()),  # start_epoch
    #     # 'submission',
    #     'comment',
    #     'corona')

    test_psaw.test_psaw_search_with_multiple_query(
        # int(dt.datetime(2020, 10, 7).timestamp()),
        int(dt.datetime(2020, 10, 10).timestamp()),
        # int(dt.datetime(2020, 9, 5).timestamp()),  # start_epoch
        # int(dt.datetime(2020, 9, 1).timestamp()),  # start_epoch
        'submission',
        'work_from_home',
        # 'corona',
    )

    # for i in ALL_ASPECTS:
    #     test_psaw.test_psaw_search_submission_with_multiple_query(i)
