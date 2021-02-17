# -*- coding: utf-8 -*-

"""Crawl data from twitter and reddit."""

import datetime
from itertools import product
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from typing import cast

import click

# from Examples.scratch2 import ALL_CRAWLERS
from global_parameters import ALL_CRAWLERS
from global_parameters import ALL_REDDIT_COLLECTION_NAMES
from global_parameters import ALL_REDDIT_RESPOND_TYPES
from global_parameters import ALL_REDDIT_SEARCH_TYPES
from global_parameters import ALL_REDDIT_TAGS
from global_parameters import ALL_SUBREDDIT_REPRESETED_COUNTRY_SUBREDDIT
from global_parameters import ALL_SUBREDDIT_REPRESETED_GENERAL_COVID_SUBREDDIT
from global_parameters import ALL_SUBREDDIT_REPRESETED_REGION_COVID_SUBREDDIT
from global_parameters import ALL_SUBREDDIT_REPRESETED_STATES_COVID_SUBREDDIT
from global_parameters import ALL_TWITTER_COLLETION_NAMES
from global_parameters import ALL_TWITTER_RESPOND_TYPES
from global_parameters import ALL_TWITTER_SEARCH_TYPES
from global_parameters import ALL_TWITTER_TAGS
from global_parameters import COVID_KEYWORDS
from global_parameters import KNOWN_ERROR
from global_parameters import LOCKDOWN_KEYWORDS
from global_parameters import REDDIT_SORT
from global_parameters import REOPEN_KEYWORDS
from global_parameters import SOCIAL_DISTANCE_KEYWORDS
from global_parameters import WORK_FROM_HOME_KEYWORDS
from src.Sources.Preparations.Data.reddit_crawler import RedditCrawler
from src.Sources.Preparations.Data.reddit_crawler import RedditCrawlerCondition
from src.Sources.Preparations.Data.reddit_crawler import run_reddit_crawler
from src.Sources.Preparations.Data.twitter_crawler import TwitterCrawler
from src.Sources.Preparations.Data.twitter_crawler import (
    TwitterCrawlerCondition,
)
from src.Sources.Preparations.Data.twitter_crawler import run_twitter_crawler
from src.Utilities import Crawler_type
from src.Utilities import Frequency
from src.Utilities import RunningConditions
from src.Utilities import RunningConditionsKeyValue
from src.Utilities import SubredditCollection
from src.Utilities import Tags
from src.Utilities import TwitterCollection
from src.Utilities import my_timer
from src.Utilities.CheckConditions.check_conditions import \
    check_crawler_tags_value
from src.Utilities.CheckConditions.check_conditions import \
    check_running_conditions
from src.Utilities.ClickLibrary.custom_commands import (
    enfore_dependency_between_date_cli_args,
)
from src.Utilities.Logging import MyLogger

LOGGER = MyLogger()
PROGRAM_LOGGER = LOGGER.program_logger


def _get_running_conditions(
        crawler_option: str,
        collection_name: str,
        search_type: str,
        respond_type: str,
        tag: str,
        max_after: int,
) -> RunningConditions:
    """
    Get common conditions (constraints) of all crawler.

    :type crawler_option: str
    :param crawler_option: crawler name

    :type collection_name: str
    :param collection_name: collection (category of data to be collected)

    :type search_type: str
    :param search_type: search_type specify how (where) you want crawler to
    crawl (largely depends on api used by each crawler option)

    :type respond_type: str
    :param respond_type:  respond_type specify types of respond you wants (any
    functions can be applied here eg. find average tweet of 5 day by username
    start with James etc)

    :type tag: None or str
    :param tag: tag or aspect

    :param max_after: int
    :param max_after: number of (previous) frequency that will be collected

    :rtype: RunningConditions
    :return: dict of common constraints for all crawlers
    """
    running_conditions_dict: RunningConditions = {
        "crawler_option": crawler_option,
        "collection_name": collection_name,
        # 'respond_type': 'data',
        "respond_type": respond_type,
        "search_type": search_type,
        "sort": REDDIT_SORT[1],
        "tag": tag,
        "max_after": max_after,
    }
    return running_conditions_dict


def run_crawler(
        run_crawler_func: Callable,
        crawler_condition: Union[
            RedditCrawlerCondition, TwitterCrawlerCondition],
) -> Tuple[int, int]:
    """Deprecate."""
    return run_crawler_func(crawler_condition)


def get_keywords_collections(crawler_type: str,
                             ALL_TWITTER_COVID_HASHTAGS=None) -> List[List[str]]:
    """Skipped summary.

    Return aspects and list of keywords (query) for each aspects with respect
    to each crawler type.

    :param crawler_type: str
    :param crawler_type: crawler name

    :rtype: tuple of list of str
    :return: aspects and list of keywords (query) for each aspects with respect
     to each crawler type
    """
    # aspects
    lockdown_keywords = LOCKDOWN_KEYWORDS
    reopen_keywords = REOPEN_KEYWORDS
    social_distance_keywords = SOCIAL_DISTANCE_KEYWORDS
    work_from_home_keywords = WORK_FROM_HOME_KEYWORDS
    covid_keywords = COVID_KEYWORDS

    if crawler_type == "reddit":

        General = ALL_SUBREDDIT_REPRESETED_GENERAL_COVID_SUBREDDIT
        Country = ALL_SUBREDDIT_REPRESETED_COUNTRY_SUBREDDIT
        Region = ALL_SUBREDDIT_REPRESETED_REGION_COVID_SUBREDDIT

        # --------List of USA States
        states_subreddit = ALL_SUBREDDIT_REPRESETED_STATES_COVID_SUBREDDIT


        return [
            General,
            Country,
            Region,
            states_subreddit,
            social_distance_keywords,
            lockdown_keywords,
            work_from_home_keywords,
            covid_keywords,
            reopen_keywords,
        ]  # noqa: E127

    elif crawler_type == "twitter":

        hashtags = ALL_TWITTER_COVID_HASHTAGS

        return [
            hashtags,
            covid_keywords,
            work_from_home_keywords,
            social_distance_keywords,
            lockdown_keywords,
            reopen_keywords,
        ]  # noqa: E127
    else:
        raise ValueError(f"Currently only support {ALL_CRAWLERS}")


def _get_crawler_tags_words(
        crawler: str,
        tag: str,
        work_from_home_keywords: List[str],
        lockdown_keywords: List[str],
        social_distance_keywords: List[str],
        corona_keywords: List[str],
        reopen_keywords: List[str],
) -> List[str]:
    if tag == "work_from_home":
        tag_words = work_from_home_keywords
    elif tag == "lockdown":
        tag_words = lockdown_keywords
    elif tag == "social_distance":
        tag_words = social_distance_keywords
    elif tag =='corona':
        tag_words = corona_keywords
    elif tag == "reopen":
        if crawler == 'twitter':
            raise NotImplementedError(
                "make sure that reddit also implement reopen_keywords "
                "allowing reopen for twitter"
            )
        tag_words = reopen_keywords
    elif tag is None:
        raise ValueError("you must provide tags for twitter")
    else:
        raise NotImplementedError(tag)

    return tag_words

def twitter_crawler_condition(
        timestamp: datetime.datetime,
        running_conditions: RunningConditions,
) -> TwitterCrawlerCondition:
    """
    Return constraint with specific format for twitter.

    :type timestamp: datetime.datetime
    :param timestamp: timestamp at the time that data is retreived (not when
        data is published)

    :type running_conditions: RunningConditions
    :param running_conditions: a dict with key specify common conditions
        (constraints) for all crawlers

    :rtype: TwitterCrawlerCondition
    :return: constraint with specific format for twitter
    """
    tag = cast(str,running_conditions["tag"])
    respond_type = running_conditions["respond_type"]
    search_type = running_conditions["search_type"]
    collection_name = running_conditions["collection_name"]
    # sort = running_conditions['sort']
    # crawler_option = running_conditions['crawler_option']
    max_after = running_conditions["max_after"]


    (
        hashtags,
        covid_keywords,
        work_from_home_keywords,
        social_distance_keywords,
        lockdown_keywords,
        reopening_keywords,
    ) = get_keywords_collections(ALL_CRAWLERS[0])

    # DEPRECATED: move to module scope
    # def _get_crawler_tags_words() -> List[str]:
    #     if tag == "work_from_home":
    #         tag_words = work_from_home_keywords
    #     elif tag == "lockdown":
    #         tag_words = lockdown_keywords
    #     elif tag == "social_distance":
    #         tag_words = social_distance_keywords
    #     elif tag == "covid":
    #         tag_words = corona_keywords
    #     elif tag == "reopen":
    #         raise NotImplementedError(
    #             "make sure that reddit also implement reopen_keywords "
    #             "allowing reopen for twitter"
    #         )
    #         tag_words = reopen_keywords
    #     elif tag is None:
    #         raise ValueError("you must provide tags for twitter")
    #     else:
    #         raise NotImplementedError(tag)
    #
    #     return tag_words

    # VALIDATE: haven't test below paragraph
    tag_words = _get_crawler_tags_words(
        crawler=ALL_CRAWLERS[0],
        tag=tag,
        work_from_home_keywords=work_from_home_keywords,
        lockdown_keywords=lockdown_keywords,
        social_distance_keywords=social_distance_keywords,
        corona_keywords=covid_keywords,
        reopen_keywords=reopening_keywords,
    )

    day_interval: int = 1
    frequency: Frequency = "day"
    if collection_name == "twitter_tweet":
        twitter_crawler_collection: TwitterCollection = {
            "collection":
                {
                    "aspect": cast(str, tag),
                    "query": tag_words
                },
            "name": collection_name,
        }

        crawler_condition: TwitterCrawlerCondition = {
            "crawler_class": TwitterCrawler,
            "collection_class": twitter_crawler_collection,
            "interval": day_interval,
            "request_timestamp": timestamp,
            "respond_type": respond_type,
            "search_type": search_type,
            "frequency": frequency,
            "tag": tag_words,
            "max_after": max_after,
        }
    elif collection_name == "twitter_geo":
        raise NotImplementedError("")
        # twitter_crawler_collection: TwitterCollection = {
        #     'collection': {'aspect': tag, 'query': tag_words +
        #       state_keywords},
        #     'name': collection_name}
        #
        # crawler_condition: TwitterCrawlerCondition = {
        #     'crawler_class': TwitterCrawler,
        #     'collection_class': twitter_crawler_collection,
        #     'interval': day_interval,
        #     'request_timestamp': timestamp,
        #     'respond_type': respond_type,
        #     'search_type': search_type,
        #     'frequency': frequency,
        #     'tag': tag_words,
        #     'max_after': max_after
        # }
    else:
        raise NotImplementedError()

    return crawler_condition


def reddit_crawler_condition(
        timestamp: datetime.datetime,
        running_conditions: RunningConditions,
) -> RedditCrawlerCondition:
    """Return constraint with specific format for reddit.

    :type timestamp: datetime.datetime
    :param timestamp: timestamp at the time that data is retreived
        (not when data is published)

    :type running_conditions: RunningConditions
    :param running_conditions: a dict with key specify common conditions
        (constraints) for all crawlers

    :rtype: RedditCrawlerCondition
    :return: constraint with specific format for Reddit
    """
    tag = cast(str, running_conditions["tag"])
    respond_type = running_conditions["respond_type"]
    search_type = running_conditions["search_type"]
    collection_name = running_conditions["collection_name"]
    # sort = running_conditions['sort']
    # crawler_option = running_conditions['crawler_option']
    max_after = running_conditions["max_after"]

    (
        General,
        Country,
        Region,
        states_subreddit,
        social_distance_keywords,
        lockdown_keywords,
        work_from_home_keywords,
        covid_keywords,
        reopening_keywords,
    ) = get_keywords_collections(ALL_CRAWLERS[1])

    # DEPRECATED: move to module scope
    # def _get_crawler_tags_words() -> List[str]:
    #     if tag == "work_from_home":
    #         tag_words = work_from_home_keywords
    #     elif tag == "lockdown":
    #         tag_words = lockdown_keywords
    #     elif tag == "social_distance":
    #         tag_words = social_distance_keywords
    #     elif tag == 'reopen':
    #         tag_words = reopening_keywords
    #     elif tag == 'covid':
    #         tag_words = covid_keywords
    #     # elif tag == 'all':
    #     #     tag_words
    #     #     raise NotImplementedError(tag)
    #     elif tag is None:
    #         tag_words = []
    #     else:
    #         raise NotImplementedError(tag)
    #
    #     return tag_words


    # VALIDATE: haven't test below paragraph
    tag_words = _get_crawler_tags_words(
        crawler=ALL_CRAWLERS[1],
        tag=tag,
        work_from_home_keywords=work_from_home_keywords,
        lockdown_keywords=lockdown_keywords,
        social_distance_keywords=social_distance_keywords,
        corona_keywords=covid_keywords,
        reopen_keywords=reopening_keywords,
    )

    subreddit_collection_class: SubredditCollection
    # initial_day_interval = 16
    initial_day_interval = 1
    frequency: Frequency = "day"

    crawler_condition: RedditCrawlerCondition

    # crawler_class: Type[RedditCrawler]
    # collection_class: SubredditCollection
    # initial_interval: int
    # request_timestamp: datetime.datetime
    # respond_type: str
    # search_type: str
    # frequency: str
    # verbose: bool
    # aspect: Optional[str]
    # max_after: int

    def _get_crawler_condition(
            subreddit_collection_class: SubredditCollection,
    ) -> RedditCrawlerCondition:

        crawler_condition: RedditCrawlerCondition = {
            "crawler_class": RedditCrawler,
            "collection_class": subreddit_collection_class,
            "initial_interval": initial_day_interval,
            "request_timestamp": timestamp,
            "respond_type": respond_type,
            "search_type": search_type,
            "frequency": frequency,
            "verbose": True,
            "max_after": max_after,
        }
        return crawler_condition

    if collection_name == "corona_general":

        subreddit_collection_class = {
            "collection": {
                "subreddit": General,
                "aspect": tag,
                "query": tag_words,
            },
            "name": collection_name,
        }

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    elif collection_name == "corona_countries":
        subreddit_collection_class = {
            "collection": {
                "subreddit": Country,
                "aspect": tag,
                "query": tag_words,
            },
            "name": collection_name,
        }

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    elif collection_name == "corona_regions":
        subreddit_collection_class = {
            "collection": {
                "subreddit": Region,
                "aspect": tag,
                "query": tag_words,
            },
            "name": collection_name,
        }

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    elif collection_name == "corona_states_with_tag":

        assert tag is not None
        tag_words = cast(List[str], tag)
        # tag_words = tag_words if tag is not None else ALL_KEYWORDS

        subreddit_collection_class = {
            "collection": {
                "subreddit": states_subreddit,
                "aspect": tag,
                "query": tag_words,
            },
            "name": collection_name,
        }

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    else:
        raise ValueError("collection_name is not supported")

    return crawler_condition


def select_crawler_condition(
        running_conditions: RunningConditions,
        timestamp: datetime.datetime,
) -> Tuple[Callable, Union[RedditCrawlerCondition, TwitterCrawlerCondition]]:
    """Return crawler and its CrawlerCondition dictionary.

    :type running_conditions: RunningConditions
    :param running_conditions: a dict with key specify common conditions
        (constraints) for all crawlers

    :type timestamp: datetime.datetime
    :param timestamp: timestamp at the time that data is retreived (not when
        data is published)

    :rtype: tuple of crawler and its CrawlerCondition dictionary
    :return: crawler and its CrawlerCondition dictionary
    """
    # timestamp = datetime.datetime.now()
    crawler_conditions: Union[RedditCrawlerCondition, TwitterCrawlerCondition]
    if running_conditions["crawler_option"] == "reddit":
        crawler_conditions = reddit_crawler_condition(
            timestamp,
            running_conditions,
        )

        return run_reddit_crawler, crawler_conditions

    elif running_conditions["crawler_option"] == "twitter":
        crawler_conditions = twitter_crawler_condition(
            timestamp,
            running_conditions,
        )
        return run_twitter_crawler, crawler_conditions
    else:
        raise ValueError(
            f'selected crawler_class == {running_conditions["crawler_option"]}'
            f" is not supported",
        )


def _get_tag_value(tags: Tags,
                   all_crawler_tags: List[str],
                   ) -> Tags:
    if tags is not None:
        check_crawler_tags_value(tags, all_crawler_tags)
        if len(tags) == 1 and tags[0] == "all":
            return all_crawler_tags
        else:
            return tags
    else:
        return [tags]


def get_reddit_running_conditions(
        before_date: datetime.datetime,
        after_date: datetime.datetime,
        max_after: int,
        tags: Tags,
        crawler_option: Crawler_type,
        get_alll_running_conditions: bool = True,
) -> Union[List, List[RunningConditionsKeyValue]]:
    """Skipped summary.

    Prepare and return list of running condition (common constraints among
        crawler) for reddit crawler.

    :param max_after: int
    :param max_after: number of (previous) frequency that will be collected

    :type tags: tuple of tags
    :param tags: tuple of tags (aspects)

    :type crawler_option: str
    :param crawler_option: crawler name

    :rtype: list of RunningConditionsKeyValue
    :return:  list of running condition (common constraints among crawler) for
        reddit crawler
    """


    # DEPRECATED: move to module scope
    # def _get_tag_value(tags: Tags) -> Tags:
    #     if tags is not None:
    #         check_reddit_tags_value(tags)
    #
    #         if len(tags) == 1 and tags[0] == "all":
    #             return ALL_REDDIT_TAGS
    #         else:
    #             return tags
    #     else:
    #         return [tags]

    # --conditions
    # tags = _get_tag_value(tags)

    tags = _get_tag_value(
        tags,
        ALL_REDDIT_TAGS,
    )

    # NOTE: I am sure if tags == None is suppported.This is worth noting for
    #     furture code clean up
    all_collection_name = (
        ALL_REDDIT_COLLECTION_NAMES
        if tags is None
        else ALL_REDDIT_COLLECTION_NAMES
    )
    all_search_type = ALL_REDDIT_SEARCH_TYPES
    all_respond_type = ALL_REDDIT_RESPOND_TYPES

    all_running_conditions_key_value: RunningConditionsKeyValue = []


    if get_alll_running_conditions:
        for max_after, tag, collection_name, search_type, respond_type in product(
                [max_after],
                cast(List[str], tags),
                all_collection_name,
                all_search_type,
                all_respond_type,
        ):
            tag_str = tag

            condition_keys: List[Union[Optional[str], int]] = [
                max_after,
                tag_str,
                collection_name,
                search_type,
            ]

            running_condition: RunningConditions = _get_running_conditions(
                crawler_option,
                collection_name,
                search_type,
                respond_type,
                tag,
                max_after,
            )
            all_running_conditions_key_value.append(
                (condition_keys, running_condition),
            )
    else:
        raise NotImplementedError("Note sure how much refactoring will be "
                                  "needed. But function-wise without ability"
                                  " to specified specific running condition,"
                                  " the program can still perfectly function")


    # selected_running_conditions = []
    # for i in all_running_conditions_key_value:
    #     if i[0][1] == 'corona_states_with_tag':
    #         selected_running_conditions.append(i[0])
    # print(selected_running_conditions)

    return all_running_conditions_key_value


def get_twitter_running_conditions(
        before_date: datetime.datetime,
        after_date: datetime.datetime,
        max_after: int,
        tags: Tags,
        crawler_option: Crawler_type,
) -> Union[List, List[RunningConditions]]:
    """Skipped summary.

    Prepare and return list of running condition (common constraints among
        crawler) for twitter crawler.

    :param max_after: int
    :param max_after: number of (previous) frequency that will be collected

    :type tags: tuple of tags
    :param tags: tuple of tags (aspects)

    :type crawler_option: str
    :param crawler_option: crawler name

    :rtype: list of RunningConditionsKeyValue
    :return:  list of running condition (common constraints among crawler) for
        twitter crawler
    """

    # DEPRECATED: move to module scope
    # def _get_tag_value(tags: Tags) -> Tags:
    #     if tags is not None:
    #         check_crawler_tags_value(tags)
    #         if len(tags) == 1 and tags[0] == "all":
    #             return ALL_TWITTER_TAGS
    #         else:
    #             return tags
    #     else:
    #         return [tags]

    tags = _get_tag_value(
        tags,
        ALL_TWITTER_TAGS,
    )

    all_collection_name = ALL_TWITTER_COLLETION_NAMES
    all_search_type = ALL_TWITTER_SEARCH_TYPES
    all_respond_type = ALL_TWITTER_RESPOND_TYPES

    all_running_conditions_key_value: RunningConditionsKeyValue = []

    for max_after, tag, collection_name, search_type, respond_type in product(
            [max_after],
            cast(List[str], tags),
            all_collection_name,
            all_search_type,
            all_respond_type,
    ):
        tag_str = tag

        condition_keys: List[Union[Optional[str], int]] = [
            max_after,
            tag_str,
            collection_name,
            search_type,
        ]

        running_condition: RunningConditions = _get_running_conditions(
            crawler_option,
            collection_name,
            search_type,
            respond_type,
            tag,
            max_after,
        )
        all_running_conditions_key_value.append(
            (condition_keys, running_condition),
        )

    # selected_running_conditions = []
    # for i in all_running_conditions_key_value:
    #     if i[0][1] == 'corona_states_with_tag':
    #         selected_running_conditions.append(i[0])
    # print(selected_running_conditions)

    return all_running_conditions_key_value

    # one_running_conditions: RunningConditions = _get_running_conditions(
    #     crawler_option, 'twitter_tweet',
    #     'data_tweet', 'data_tweet', tags, max_after)

    # two_running_conditions: RunningConditions = _get_running_conditions(
    #     crawler_option, 'twitter_geo',
    #     'data_geo', 'data_geo', tags, max_after)

    # all_running_conditions = []
    # all_running_conditions.append(one_running_conditions)
    # # all_running_conditions.append(two_running_conditions)

    # tmp = []
    # for i in all_running_conditions:
    #     tag = i['tag']
    #     collection_name = i['collection_name']
    #     search_type = i['search_type']
    #     tmp.append(([tag, collection_name, search_type], i))
    # all_running_conditions = tmp

    # return all_running_conditions


def get_crawler_running_conditions(
        before_date: datetime.datetime,
        after_date: datetime.datetime,
        max_after: int,
        tags: Tags,
        crawler_type: Crawler_type,
) -> Union[List, List[RunningConditions]]:
    """Skipped summary.

    Prepare and return list of running condition (common constraints among
        crawler) for a specified crawler.

    :param max_after: int
    :param max_after: number of (previous) frequency that will be collected

    :type tags: tuple of tags
    :param tags: tuple of tags (aspects)

    :type crawler_option: str
    :param crawler_option: crawler name

    :rtype: list of RunningConditionsKeyValue
    :return:  list of running condition (common constraints among crawler) for
        specified crawler
    """
    if crawler_type == "reddit":
        return get_reddit_running_conditions(
            before_date,
            after_date,
            max_after,
            tags,
            crawler_type,
        )
    elif crawler_type == "twitter":
        return get_twitter_running_conditions(
            before_date,
            after_date,
            max_after,
            tags,
            crawler_type,
        )

    else:
        raise ValueError("you must select between reddit or twitter crawler ")


def run_all_reddit_conditions(
        before_date: datetime.datetime,
        after_date: datetime.datetime,
        max_after: int,
        tags: Tags,
        timestamp: datetime.datetime,
        crawler_type: Crawler_type,
):
    """
    Run all of reddit conditions.

    :type before_date: datetime.datetime
    :param before_date: date in which all aata BEFORE this date should be
        retrieved

    :type after_date: datetime.datetime
    :param after_date: date in which all aata AFTER this date should be
        retrieved

    :param max_after: int
    :param max_after: number of (previous) frequency that will be collected

    :type tags: tuple of tags
    :param tags: tuple of tags (aspects)

    :type timestamp: datetime.datetime
    :param timestamp: timestamp at the time that data is retreived (not when
        data is published)

    :param crawler_type: str
    :param crawler_type: crawler name

    """
    # FIXME: before_date and after_date is not implemented because it is not
    #  compatible with the current convention that use Max_after

    total_returned_data, total_missing_data = 0, 0

    all_running_conditions = get_crawler_running_conditions(
        before_date,
        after_date,
        max_after,
        tags,
        crawler_type,
    )

    # all_running_conditions = all_reddit_running_conditions

    for (i, (condition_keys, running_conditions)) in enumerate(
            all_running_conditions[1:],
    ):
        check_running_conditions(running_conditions)

        run_crawler_func, crawler_condition = select_crawler_condition(
            running_conditions=running_conditions,
            timestamp=timestamp,
        )
        try:
            (
                total_returned_data_per_run,
                total_missing_data_per_run,
            ) = run_crawler(run_crawler_func, crawler_condition)
            total_returned_data += total_returned_data_per_run
            total_missing_data += total_missing_data_per_run
        except Exception as e:
            if str(e) not in KNOWN_ERROR:
                PROGRAM_LOGGER.error(str(e))
                raise NotImplementedError(
                    f"unknown error occur in {run_all_conditions.__name__}."
                    f"{str(e)}",
                )

            else:
                PROGRAM_LOGGER.error(
                    f"!!!! The following error occurs = {str(e)} !!!")
                condition_keys_str: str = ",".join(map(str, condition_keys))

                if i == len(all_running_conditions) - 1:
                    PROGRAM_LOGGER.error(
                        f" || skip the the current condition "
                        f"= ({condition_keys_str}) "
                        f"==> No more running conditions to run "
                        f"==> exiting {run_all_conditions.__name__}() \n",
                    )
                else:
                    next_condition_keys \
                        = all_running_conditions[i + 1][0]  # type: ignore
                    next_condition_keys_str: str = ",".join(
                        map(str, next_condition_keys),
                    )
                    PROGRAM_LOGGER.error(
                        f" || skip the the current condition = "
                        f"({condition_keys_str}) "
                        f"==> start next running condition "
                        f"= {next_condition_keys_str} \n",
                    )
    #
    PROGRAM_LOGGER.info(
        f" || total_returned_data = {total_returned_data} "
        f"|| total_missing_data = {total_missing_data}",
    )


def run_all_twitter_conditions(
        before_date: datetime.datetime,
        after_date: datetime.datetime,
        max_after: int,
        tags: Tags,
        timestamp: datetime.datetime,
        crawler_type: Crawler_type,
) -> None:
    """
    Run all of twitter conditions.

    :type before_date: datetime.datetime
    :param before_date: date in which all aata BEFORE this date should be
        retrieved

    :type after_date: datetime.datetime
    :param after_date: date in which all aata AFTER this date should be
        retrieved

    :param max_after: int
    :param max_after: number of (previous) frequency that will be collected

    :type tags: tuple of tags
    :param tags: tuple of tags (aspects)

    :type timestamp: datetime.datetime
    :param timestamp: timestamp at the time that data is retreived (not when
        data is published)

    :param crawler_type: str
    :param crawler_type: crawler name

    """
    # FIXME: before_date and after_date is not implemented because it is not
    #  compatible with the current convention that use Max_after

    total_returned_data, _ = 0, 0

    all_running_conditions = get_crawler_running_conditions(
        before_date,
        after_date,
        max_after,
        tags,
        crawler_type,
    )

    for (_i, (_condition_keys, running_conditions)) in enumerate(
            all_running_conditions,
    ):
        check_running_conditions(running_conditions)

        run_crawler_func, crawler_condition = select_crawler_condition(
            running_conditions=running_conditions,
            timestamp=timestamp,
        )

        try:
            (
                total_returned_data_per_run,
                total_missing_data_per_run
            ) = run_crawler(
                run_crawler_func,
                crawler_condition,
            )

            total_returned_data += total_returned_data_per_run

        except Exception as e:
            if str(e) not in KNOWN_ERROR:

                raise NotImplementedError(
                    f"unknown error occur in {run_all_conditions.__name__} ",
                )

            else:
                PROGRAM_LOGGER.error(
                    f"!!!! The following error occurs = {str(e)} in "
                    f"{run_all_conditions.__name__}!!!",
            )


    PROGRAM_LOGGER.info(f" || total_returned_data = {total_returned_data}")


def run_all_conditions(
        before_date: datetime.datetime,
        after_date: datetime.datetime,
        max_after: int,
        tags: Tags,
        crawler_type: Crawler_type,
):
    """Run all of specified crawler conditions.

    :type before_date: datetime.datetime
    :param before_date: date in which all aata BEFORE this date should be
        retrieved

    :type after_date: datetime.datetime
    :param after_date: date in which all aata AFTER this date should be
        retrieved

    :param max_after: int
    :param max_after: number of (previous) frequency that will be collected

    :type tags: tuple of tags
    :param tags: tuple of tags (aspects)

    :type timestamp: datetime.datetime
    :param timestamp: timestamp at the time that data is retreived (not when
        data is published)

    :param crawler_type: str
    :param crawler_type: crawler name

    """
    timestamp = datetime.datetime.now()
    # print(f">>> start running all {crawler_type} conditions... <<<")
    PROGRAM_LOGGER.info(
        f">>> start running all {crawler_type} conditions... <<<")
    PROGRAM_LOGGER.info(
        f"next things ")
    PROGRAM_LOGGER.info(
        f"the next things")

    if crawler_type == "reddit":
        run_all_reddit_conditions(
            before_date,
            after_date,
            max_after,
            tags,
            timestamp,
            crawler_type,
        )
    elif crawler_type == "twitter":
        run_all_twitter_conditions(
            before_date,
            after_date,
            max_after,
            tags,
            timestamp,
            crawler_type,
        )
    elif crawler_type == "all":
        run_all_reddit_conditions(
            before_date,
            after_date,
            max_after,
            tags,
            timestamp,
            "reddit",
        )
        run_all_twitter_conditions(
            before_date,
            after_date,
            max_after,
            tags,
            timestamp,
            "twitter",
        )
    else:
        raise ValueError("your selected crawler_type is not implementd")


@click.command(cls=enfore_dependency_between_date_cli_args())
@click.argument("tags", nargs=-1, type=click.STRING)
@click.option(
    "--select_all_conditions/--select_one_condition",
    default=False)
# NOTE: default is set to tuple() when multiple=True, regardless of default
#   set to None
# @click.option("--tags", multiple=True, type=click.STRING)
@click.option("--max_after", type=int)
@click.option(
    "--before_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    # default=str(datetime.date.today()),
)
@click.option("--after_date", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option(
    "--crawler_type",
    type=click.Choice(["reddit", "twitter", "all"]),
)
@click.option("--dry_run/--no_dry_run", default=False)
@my_timer
def main(
        tags: Tags,
        select_all_conditions: bool,
        max_after: int,
        crawler_type: str,
        before_date: datetime.datetime,
        after_date: datetime.datetime,
        dry_run: bool,
) -> None:
    """Prepare input parameters and run all of specified crawler conditions.

    :type before_date: datetime.datetime
    :param before_date: date in which all aata BEFORE this date should be
    retrieved

    :type after_date: datetime.datetime
    :param after_date: date in which all aata AFTER this date should be
    retrieved

    :param max_after: int
    :param max_after: number of (previous) frequency that will be collected

    :type tags: tuple of tags
    :param tags: tuple of tags (aspects)

    :type timestamp: datetime.datetime
    :param timestamp: timestamp at the time that data is retreived (not when
    data is published)

    :param crawler_type: str
    :param crawler_type: crawler name

    """
    if dry_run:

        click.echo(
            f"We have passed in the following input args\n"
            f"\tselect_all_conditions = {select_all_conditions}\n"
            f"\ttags = {tags}\n"
            f"\tmax_after = {max_after}\n"
            f"\tcrawler_type = {crawler_type}\n"
            f"\tbefore_date = {before_date}\n"
            f"\tafter_date = {after_date}"
        )

    else:

        if isinstance(tags, tuple):
            tags = list(tags)
        elif isinstance(tags, List):
            pass
        else:
            raise TypeError

        assert len(tags) > 0


        # tags = None if len(tags) == 0 else tags
        if select_all_conditions:
            run_all_conditions(
                before_date,
                after_date,
                max_after,
                tags,
                crawler_type,
            )
        else:
            raise NotImplementedError

    PROGRAM_LOGGER.info(">>>> exit program <<<<<")


if __name__ == "__main__":
    main()
