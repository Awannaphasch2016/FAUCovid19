# -*- coding: utf-8 -*-

"""Crawl data from twitter and reddit"""

import datetime
from itertools import product
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import click

from Tests.check_conditions import _check_reddit_tags_value
from Tests.check_conditions import check_running_conditions
from global_parameters import ALL_REDDIT_COLLECTION_NAMES
from global_parameters import ALL_REDDIT_RESPOND_TYPES
from global_parameters import ALL_REDDIT_SEARCH_TYPES
from global_parameters import ALL_REDDIT_TAGS
from global_parameters import ALL_TWITTER_COLLETION_NAMES
from global_parameters import ALL_TWITTER_RESPOND_TYPES
from global_parameters import ALL_TWITTER_SEARCH_TYPES
from global_parameters import ALL_TWITTER_TAGS
from global_parameters import COVID_KEYWORDS
from global_parameters import KNOWN_ERROR
from global_parameters import LOCKDOWN_KEYWORDS
from global_parameters import MAX_AFTER
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


def _get_running_conditions(
    crawler_option: str,
    collection_name: str,
    search_type: str,
    respond_type: str,
    tag: Optional[str],
    max_after: int,
) -> RunningConditions:
    """
    get common conditions (constraints) of all crawler

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
        "sort": "asc",
        "tag": tag,
        "max_after": max_after,
    }
    return running_conditions_dict


def run_crawler(
    run_crawler_func: Callable,
    crawler_condition: Union[RedditCrawlerCondition, TwitterCrawlerCondition],
) -> Tuple[int, int]:
    """FIXME: this function should be removed and simply replaced by
    run_crawler_func()"""
    return run_crawler_func(crawler_condition)


def get_keywords_collections(crawler_type: str) -> Tuple[str]:
    """
    return aspects and list of keywords (query) for each aspects with respect
    to each crawler type

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
        General = ["Corona", "COVID19", "China_Flu", "coronavirus"]
        Country = ["CoronavirusUS", "coronavirusUK"]
        Region = [
            "CoronavirusMidwest",
            "CoronavirusSouth",
            "CoronavirusSouthEast",
            "CoronavirusWest",
        ]

        # --------List of USA States
        states_subreddit = [
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

        return (
            General,
            Country,
            Region,
            states_subreddit,
            social_distance_keywords,
            lockdown_keywords,
            work_from_home_keywords,
            covid_keywords,
            reopen_keywords,
        )  # noqa: E127

    elif crawler_type == "twitter":
        # coronavirus, #coronavirusoutbreak, #coronavirusPandemic, #covid19,
        # #covid_19, #epitwitter, #ihavecorona
        hashtags = [
            "#coronavirus",
            "#coronavirusoutbreak",
            "#coronavirusPandemic",
            "#covid19",
            "#covid_19",
            "#epitwitter",
            "#ihavecorona",
        ]

        return (
            hashtags,
            covid_keywords,
            work_from_home_keywords,
            social_distance_keywords,
            lockdown_keywords,
            reopen_keywords,
        )  # noqa: E127


def twitter_crawler_condition(
    timestamp: datetime.datetime, running_conditions: RunningConditions
) -> TwitterCrawlerCondition:
    """
    return constraint with specific format for twitter


    :type timestamp: datetime.datetime
    :param timestamp: timestamp at the time that data is retreived (not when
    data is published)

    :type running_conditions: RunningConditions
    :param running_conditions: a dict with key specify common conditions
    (constraints) for all crawlers

    :rtype: TwitterCrawlerCondition
    :return: constraint with specific format for twitter
    """

    tag = running_conditions["tag"]
    respond_type = running_conditions["respond_type"]
    search_type = running_conditions["search_type"]
    collection_name = running_conditions["collection_name"]
    # sort = running_conditions['sort']
    # crawler_option = running_conditions['crawler_option']
    max_after = running_conditions["max_after"]

    (
        hashtags,
        corona_keywords,
        work_from_home_keywords,
        social_distance_keywords,
        lockdown_keywords,
        reopen_keywords,
    ) = get_keywords_collections("twitter")

    def _get_tags_words() -> List[str]:
        if tag == "work_from_home":
            tag_words = work_from_home_keywords
        elif tag == "lockdown":
            tag_words = lockdown_keywords
        elif tag == "social_distance":
            tag_words = social_distance_keywords
        elif tag == "covid":
            tag_words = corona_keywords
        elif tag == "reopen":
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

    tag_words = _get_tags_words()

    day_interval: int = 1
    frequency: Frequency = "day"

    if collection_name == "twitter_tweet":
        twitter_crawler_collection: TwitterCollection = {
            "collection": {"aspect": tag, "query": tag_words},
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
    timestamp: datetime.datetime, running_conditions: RunningConditions
) -> RedditCrawlerCondition:
    """
    return constraint with specific format for reddit


    :type timestamp: datetime.datetime
    :param timestamp: timestamp at the time that data is retreived
        (not when data is published)

    :type running_conditions: RunningConditions
    :param running_conditions: a dict with key specify common conditions
        (constraints) for all crawlers

    :rtype: RedditCrawlerCondition
    :return: constraint with specific format for Reddit
    """

    tag = running_conditions["tag"]
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
    ) = get_keywords_collections("reddit")

    def _get_tags_words() -> List[str]:
        if tag == "work_from_home":
            tag_words = work_from_home_keywords
        elif tag == "lockdown":
            tag_words = lockdown_keywords
        elif tag == "social_distance":
            tag_words = social_distance_keywords
        # elif tag == 'all':
        #     tag_words
        #     raise NotImplementedError(tag)
        elif tag is None:
            tag_words = []
        else:
            raise NotImplementedError(tag)

        return tag_words

    # OPTIMIZE: figure out how to deal 2 versio of the same thing:
    #    eg work_from_home, work_from_home_words

    tag_words = _get_tags_words()
    subreddit_collection_class: SubredditCollection
    # initial_day_interval = 16
    initial_day_interval = 1
    frequency = "day"

    crawler_condition: RedditCrawlerCondition

    def _get_crawler_condition(
        subreddit_collection_class: SubredditCollection,
    ) -> RedditCrawlerCondition:
        crawler_condition = {
            "crawler_class": RedditCrawler,
            "collection_class": subreddit_collection_class,
            "initial_interval": initial_day_interval,  # 100
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
        tag_words = tag
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
    running_conditions: RunningConditions, timestamp: datetime.datetime
) -> Tuple[Callable, Union[RedditCrawlerCondition, TwitterCrawlerCondition]]:
    """
    return crawler and its CrawlerCondition dictionary

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
            timestamp, running_conditions
        )

        return run_reddit_crawler, crawler_conditions

    elif running_conditions["crawler_option"] == "twitter":
        crawler_conditions = twitter_crawler_condition(
            timestamp, running_conditions
        )
        return run_twitter_crawler, crawler_conditions
    else:
        raise ValueError(
            f'selected crawler_class == {running_conditions["crawler_option"]}'
            f" is not supported"
        )


def get_reddit_running_conditions(
    before_date: datetime.datetime,
    after_date: datetime.datetime,
    max_after: int,
    tags: Tags,
    crawler_option: Crawler_type,
) -> Union[List, List[RunningConditionsKeyValue]]:
    """
    prepare and return list of running condition (common constraints among
        crawler) for reddit crawler

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

    def _get_tag_value(tags: Tags) -> Tags:
        if tags is not None:
            _check_reddit_tags_value(tags)

            if len(tags) == 1 and tags[0] == "all":
                return ALL_REDDIT_TAGS
            else:
                return tags
        else:
            return [tags]

    # --conditions
    tags = _get_tag_value(tags)

    all_collection_name = (
        ALL_REDDIT_COLLECTION_NAMES
        if tags is None
        else ALL_REDDIT_COLLECTION_NAMES
    )
    all_search_type = ALL_REDDIT_SEARCH_TYPES
    all_respond_type = ALL_REDDIT_RESPOND_TYPES

    all_running_conditions_key_value: RunningConditionsKeyValue = []

    for max_after, tag, collection_name, search_type, respond_type in product(
        [max_after],
        tags,
        all_collection_name,
        all_search_type,
        all_respond_type,
    ):
        tag_str = tag

        condition_keys: List[Optional[str], int] = [
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
            (condition_keys, running_condition)
        )

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
    """
    prepare and return list of running condition (common constraints among
        crawler) for twitter crawler

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

    def _get_tag_value(tags: Tags) -> Tags:
        if tags is not None:
            _check_reddit_tags_value(tags)
            if len(tags) == 1 and tags[0] == "all":
                return ALL_TWITTER_TAGS
            else:
                return tags
        else:
            return [tags]

    tags = _get_tag_value(tags)

    all_collection_name = ALL_TWITTER_COLLETION_NAMES
    all_search_type = ALL_TWITTER_SEARCH_TYPES
    all_respond_type = ALL_TWITTER_RESPOND_TYPES

    all_running_conditions_key_value: RunningConditionsKeyValue = []

    for max_after, tag, collection_name, search_type, respond_type in product(
        [max_after],
        tags,
        all_collection_name,
        all_search_type,
        all_respond_type,
    ):
        tag_str = tag

        condition_keys: List[Optional[str], int] = [
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
            (condition_keys, running_condition)
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
    """
    prepare and return list of running condition (common constraints among
        crawler) for a specified crawler

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
            before_date, after_date, max_after, tags, crawler_type
        )
    elif crawler_type == "twitter":
        return get_twitter_running_conditions(
            before_date, after_date, max_after, tags, crawler_type
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
    run all of reddit conditions

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
        before_date, after_date, max_after, tags, crawler_type
    )

    # all_running_conditions = all_reddit_running_conditions

    for (i, (condition_keys, running_conditions)) in enumerate(
        all_running_conditions[1:]
    ):
        check_running_conditions(running_conditions)

        run_crawler_func, crawler_condition = select_crawler_condition(
            running_conditions=running_conditions, timestamp=timestamp
        )
        try:
            (
                total_returned_data_per_run,
                total_missing_data_per_run,
            ) = run_crawler(run_crawler_func, crawler_condition)
            total_returned_data += total_returned_data_per_run
            total_missing_data += total_missing_data_per_run
            print()
        except Exception as e:
            if str(e) not in KNOWN_ERROR:
                print(str(e))
                raise NotImplementedError(
                    f"unknown error occur in {run_all_conditions.__name__} "
                )

            else:
                print(f"!!!! The following error occurs = {str(e)} !!!")
                condition_keys_str: str = ",".join(map(str, condition_keys))

                if i == len(all_running_conditions) - 1:
                    print(
                        f" || skip the the current condition "
                        f"= ({condition_keys_str}) "
                        f"==> No more running conditions to run "
                        f"==> exiting {run_all_conditions.__name__}()"
                    )
                    print()
                else:
                    next_condition_keys = all_running_conditions[i + 1][0]
                    next_condition_keys_str: str = ",".join(
                        map(str, next_condition_keys)
                    )
                    print(
                        f" || skip the the current condition = "
                        f"({condition_keys_str}) "
                        f"==> start next running condition "
                        f"= {next_condition_keys_str} "
                    )
                    print()
    #
    print(
        f" || total_returned_data = {total_returned_data} "
        f"|| total_missing_data = {total_missing_data}"
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
    run all of twitter conditions

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
        before_date, after_date, max_after, tags, crawler_type
    )

    for (i, (condition_keys, running_conditions)) in enumerate(
        all_running_conditions
    ):
        check_running_conditions(running_conditions)

        run_crawler_func, crawler_condition = select_crawler_condition(
            running_conditions=running_conditions, timestamp=timestamp
        )

        try:

            total_returned_data_per_run = run_crawler(
                run_crawler_func, crawler_condition
            )
            total_returned_data += total_returned_data_per_run
            print()
        except Exception as e:
            if str(e) not in KNOWN_ERROR:

                raise NotImplementedError(
                    f"unknown error occur in {run_all_conditions.__name__} "
                )

            else:
                print(
                    f"!!!! The following error occurs = {str(e)} in "
                    f"{run_all_conditions.__name__}!!!"
                )

    print(f" || total_returned_data = {total_returned_data}")


def run_all_conditions(
    before_date: datetime.datetime,
    after_date: datetime.datetime,
    max_after: int,
    tags: Tags,
    crawler_type: Crawler_type,
):
    """
    run all of specified crawler conditions

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
    print(f">>> start running all {crawler_type} conditions... <<<")
    if crawler_type == "reddit":
        run_all_reddit_conditions(
            before_date, after_date, max_after, tags, timestamp, crawler_type
        )
    elif crawler_type == "twitter":
        run_all_twitter_conditions(
            before_date, after_date, max_after, tags, timestamp, crawler_type
        )
    elif crawler_type == "all":
        run_all_reddit_conditions(
            before_date, after_date, max_after, tags, timestamp, "reddit"
        )
        run_all_twitter_conditions(
            before_date, after_date, max_after, tags, timestamp, "twitter"
        )
    else:
        raise ValueError("your selected crawler_type is not implementd")


@click.command()
@click.option("--select_all_conditions/--select_one_condition", default=False)
# NOTE: default is set to tuple() when multiple=True, regardless of default
#   set to None
@click.option("--tags", multiple=True, type=click.STRING)
@click.option("--max_after", type=int, default=MAX_AFTER)
@click.option(
    "--before_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(datetime.date.today()),
)
@click.option("--after_date", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option(
    "--crawler_type", type=click.Choice(["reddit", "twitter", "all"])
)
# @click.argument('tags', nargs=-1)
@my_timer
def main(
    select_all_conditions: bool,
    tags: Tags,
    max_after: int,
    crawler_type: str,
    before_date: datetime.datetime,
    after_date: datetime.datetime,
) -> None:
    """
    prepare input parameters and run all of specified crawler conditions

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

    tags = None if len(tags) == 0 else tags
    if select_all_conditions:
        run_all_conditions(
            before_date, after_date, max_after, tags, crawler_type
        )
    else:
        raise NotImplementedError

    print(">>>> exit program <<<<<")


if __name__ == "__main__":
    main()