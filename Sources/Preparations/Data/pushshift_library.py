<<<<<<< HEAD
from global_parameters import BASE_DIR
from itertools import product

from global_parameters import ALL_TWITTER_KEYWORDS, ALL_REDDIT_COLLECTION_NAMES, ALL_KEYWORDS
from global_parameters import LOCKDOWN_KEYWORDS, REOPEN_KEYWORDS, SOCIAL_DISTANCE_KEYWORDS, WORK_FROM_HOME_KEYWORDS, COVID_KEYWORDS

import datetime
from Utilities.declared_typing import Crawler_type
=======
import sys

from Utilities.declared_typing import Crawler_type

sys.path.append("C:/Users/Anak/PycharmProjects/Covid19CookieCutter")
sys.path.append("C:/Users/Anak/PycharmProjects/Covid19CookieCutter/Sources")

import datetime
>>>>>>> fixed .gitignore to remove Output/ and add Example/
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import click

from Sources.Preparations.Data.RedditCrawler import RedditCrawler
from Sources.Preparations.Data.RedditCrawler import RedditCrawlerCondition
from Sources.Preparations.Data.RedditCrawler import run_reddit_crawler
from Sources.Preparations.Data.TwitterCrawler import TwitterCrawler
from Sources.Preparations.Data.TwitterCrawler import TwitterCrawlerCondition
from Sources.Preparations.Data.TwitterCrawler import run_twitter_crawler
from Test_dir.test_conditions import _check_reddit_tags_value
from Test_dir.test_conditions import check_running_conditions
from Utilities import my_timer
from Utilities.declared_typing import Frequency
from Utilities.declared_typing import RunningConditions
from Utilities.declared_typing import RunningConditionsKeyValue
from Utilities.declared_typing import SubredditCollection
from Utilities.declared_typing import Tags
from Utilities.declared_typing import TwitterCollection
<<<<<<< HEAD
from global_parameters import ALL_REDDIT_TAGS
from global_parameters import ALL_REDDIT_SEARCH_TYPES, ALL_REDDIT_RESPOND_TYPES
from global_parameters import ALL_TWITTER_COLLETION_NAMES, ALL_TWITTER_TAGS, ALL_TWITTER_SEARCH_TYPES, ALL_TWITTER_RESPOND_TYPES
from global_parameters import KNOWN_ERROR
from global_parameters import MAX_AFTER
from collections.abc import Iterable
=======
from global_parameters import ALL_REDDIT_COLLETION_NAMES
from global_parameters import ALL_REDDIT_TAGS
from global_parameters import ALL_SEARCH_TYPES
from global_parameters import KNOWN_ERROR
>>>>>>> fixed .gitignore to remove Output/ and add Example/


def _get_running_conditions(crawler_option: str,
                            collection_name: str,
                            search_type: str,
<<<<<<< HEAD
                            respond_type: str,
                            tag: Optional[str],
                            max_after: int,
=======
                            tag: Optional[str]
>>>>>>> fixed .gitignore to remove Output/ and add Example/
                            ) -> RunningConditions:
    running_conditions_dict: RunningConditions = {
        'crawler_option': crawler_option,
        'collection_name': collection_name,
<<<<<<< HEAD
        # 'respond_type': 'data',
        'respond_type': respond_type,
        'search_type': search_type,
        'sort': 'asc',
        'tag': tag,
        'max_after': max_after
=======
        'respond_type': 'data',
        'search_type': search_type,
        'sort': 'asc',
        'tag': tag
>>>>>>> fixed .gitignore to remove Output/ and add Example/
    }
    return running_conditions_dict


def run_crawler(run_crawler_func: Callable, crawler_condition: Union[
    RedditCrawlerCondition, TwitterCrawlerCondition],
<<<<<<< HEAD
) -> Tuple[int, int]:
    return run_crawler_func(crawler_condition)


def get_keywords_collections(crawler_type: str) -> Tuple[str]:

    # aspects

    lockdown_keywords = LOCKDOWN_KEYWORDS
    reopen_keywords = REOPEN_KEYWORDS
    social_distance_keywords = SOCIAL_DISTANCE_KEYWORDS
    work_from_home_keywords = WORK_FROM_HOME_KEYWORDS
    covid_keywords = COVID_KEYWORDS

=======
                ) -> Tuple[int, int]:
    return run_crawler_func(crawler_condition)


def get_keywords_collections(crawler_type: str):
>>>>>>> fixed .gitignore to remove Output/ and add Example/
    if crawler_type == 'reddit':
        General = ['Corona', 'COVID19', 'China_Flu', 'coronavirus']
        Country = ['CoronavirusUS', 'coronavirusUK']
        Region = ['CoronavirusMidwest', 'CoronavirusSouth',
                  'CoronavirusSouthEast',
                  'CoronavirusWest']

        # --------List of USA States
        states_subreddit = ['alabama', 'alaska', 'arizona', 'arkansas',
                            'california',
                            'colorado', 'connecticut', 'delaware', 'florida',
                            'georgia',
                            'hawaii', 'idaho', 'illinois', 'indiana', 'iowa',
                            'kansas', 'kentucky',
                            'louisiana', 'maine', 'maryland', 'massachusetts',
                            'michigan', 'minnesota', 'mississippi',
                            'missouri', 'montana', 'nebraska', 'nevada',
                            'newhampshire',
                            'newjersey', 'newmexico', 'newyork',
                            'northcarolina',
                            'northdakota', 'ohio',
                            'oklahoma', 'oregon', 'pennsylvania', 'rhodeisland',
                            'southcarolina', 'southdakota', 'tennessee',
                            'texas',
                            'utah', 'vermont', 'virginia',
                            'washington', 'westvirginia', 'wisconsin',
                            'wyoming']

<<<<<<< HEAD
        return General, Country, Region, states_subreddit, \
            social_distance_keywords, lockdown_keywords, work_from_home_keywords, covid_keywords, reopen_keywords
=======
        work_from_home = ['remote work', 'workonline']
        social_distance = []
        lock_down = []

        social_distance_words = ['social distance', 'social distancing']
        lockdown_words = ['quarantine', 'isolation', 'quarantining', 'lockdown',
                          'isolate']
        work_from_home_words = ['work from home', 'work online', 'remote work',
                                'online learning', 'distance learning']
        covid_words = ['covid', 'corona', 'sarscov2']

        return General, Country, Region, states_subreddit, work_from_home, social_distance, lock_down, \
               social_distance_words, lockdown_words, work_from_home_words, covid_words
>>>>>>> fixed .gitignore to remove Output/ and add Example/

    elif crawler_type == 'twitter':
        # coronavirus, #coronavirusoutbreak, #coronavirusPandemic, #covid19, #covid_19, #epitwitter, #ihavecorona
        hashtags = ['#coronavirus', '#coronavirusoutbreak',
                    '#coronavirusPandemic', '#covid19', '#covid_19',
                    '#epitwitter', '#ihavecorona']
<<<<<<< HEAD

        return hashtags, covid_keywords, work_from_home_keywords, social_distance_keywords, lockdown_keywords, reopen_keywords
=======
        corona_keywords = ['corona', 'covid']
        state_keywords = ['alabama', 'alaska', 'arizona', 'arkansas',
                          'california',
                          'colorado', 'connecticut', 'delaware', 'florida',
                          'georgia',
                          'hawaii', 'idaho', 'illinois', 'indiana', 'iowa',
                          'kansas', 'kentucky',
                          'louisiana', 'maine', 'maryland', 'massachusetts',
                          'michigan', 'minnesota', 'mississippi',
                          'missouri', 'montana', 'nebraska', 'nevada',
                          'newhampshire',
                          'newjersey', 'newmexico', 'newyork',
                          'northcarolina',
                          'northdakota', 'ohio',
                          'oklahoma', 'oregon', 'pennsylvania', 'rhodeisland',
                          'southcarolina', 'southdakota', 'tennessee',
                          'texas',
                          'utah', 'vermont', 'virginia',
                          'washington', 'westvirginia', 'wisconsin',
                          'wyoming']

        return hashtags, corona_keywords, state_keywords
>>>>>>> fixed .gitignore to remove Output/ and add Example/


def twitter_crawler_condition(
        timestamp: datetime.datetime,
        running_conditions: RunningConditions) -> TwitterCrawlerCondition:
<<<<<<< HEAD

    tag = running_conditions['tag']
    respond_type = running_conditions['respond_type']
    search_type = running_conditions['search_type']
    collection_name = running_conditions['collection_name']
    sort = running_conditions['sort']
    crawler_option = running_conditions['crawler_option']
    max_after = running_conditions['max_after']

    (
        hashtags, corona_keywords, work_from_home_keywords,
        social_distance_keywords, lockdown_keywords, reopen_keywords) = get_keywords_collections('twitter')

    def _get_tags_words() -> List[str]:
        if tag == 'work_from_home':
            tag_words = work_from_home_keywords
        elif tag == 'lockdown':
            tag_words = lockdown_keywords
        elif tag == 'social_distance':
            tag_words = social_distance_keywords
        elif tag == 'covid':
            tag_words = corona_keywords
        elif tag == 'reopen':
            raise NotImplementedError(
                "make sure that reddit also implement reopen_keywords allowing reopen for twitter")
            tag_words = reopen_keywords
        elif tag is None:
            raise ValueError('you must provide tags for twitter')
        else:
            raise NotImplementedError(tag)

        return tag_words

    tag_words = _get_tags_words()

    day_interval: int = 1
    frequency: Frequency = 'day'

    if collection_name == 'twitter_tweet':
        twitter_crawler_collection: TwitterCollection = {
            'collection': {'aspect': tag, 'query': tag_words},
            'name': collection_name}
=======
    hashtags, corona_keywords, state_keywords = get_keywords_collections(
        'twitter')

    day_interval: int = 10
    frequency: Frequency = 'day'

    if running_conditions['collection_name'] == 'twitter_tweet':
        twitter_crawler_collection: TwitterCollection = {
            'collection': corona_keywords,
            'name':
                running_conditions[
                    'collection_name']}
>>>>>>> fixed .gitignore to remove Output/ and add Example/

        crawler_condition: TwitterCrawlerCondition = {
            'crawler_class': TwitterCrawler,
            'collection_class': twitter_crawler_collection,
            'interval': day_interval,
            'request_timestamp': timestamp,
<<<<<<< HEAD
            'respond_type': respond_type,
            'search_type': search_type,
            'frequency': frequency,
            'tag': tag_words,
            'max_after': max_after
        }
    elif collection_name == 'twitter_geo':
        raise NotImplementedError('')
        twitter_crawler_collection: TwitterCollection = {
            'collection': {'aspect': tag, 'query': tag_words + state_keywords},
            'name': collection_name}
=======
            'respond_type': running_conditions['respond_type'],
            'search_type': running_conditions['search_type'],
            'frequency': frequency
        }
    elif running_conditions['collection_name'] == 'twitter_geo':
        twitter_crawler_collection: TwitterCollection = {
            'collection': corona_keywords + state_keywords,
            'name':
                running_conditions[
                    'collection_name']}
>>>>>>> fixed .gitignore to remove Output/ and add Example/

        crawler_condition: TwitterCrawlerCondition = {
            'crawler_class': TwitterCrawler,
            'collection_class': twitter_crawler_collection,
            'interval': day_interval,
            'request_timestamp': timestamp,
<<<<<<< HEAD
            'respond_type': respond_type,
            'search_type': search_type,
            'frequency': frequency,
            'tag': tag_words,
            'max_after': max_after
=======
            'respond_type': running_conditions['respond_type'],
            'search_type': running_conditions['search_type'],
            'frequency': frequency
>>>>>>> fixed .gitignore to remove Output/ and add Example/
        }
    else:
        raise NotImplementedError()

    return crawler_condition


def reddit_crawler_condition(
        timestamp: datetime.datetime,
        running_conditions: RunningConditions) -> RedditCrawlerCondition:
<<<<<<< HEAD

    tag = running_conditions['tag']
    respond_type = running_conditions['respond_type']
    search_type = running_conditions['search_type']
    collection_name = running_conditions['collection_name']
    sort = running_conditions['sort']
    crawler_option = running_conditions['crawler_option']
    max_after = running_conditions['max_after']

    (
        General, Country, Region, states_subreddit,
        social_distance_keywords, lockdown_keywords, work_from_home_keywords,
        covid_keywords, reopening_keywords) = get_keywords_collections('reddit')

    def _get_tags_words() -> List[str]:
        if tag == 'work_from_home':
            tag_words = work_from_home_keywords
        elif tag == 'lockdown':
            tag_words = lockdown_keywords
        elif tag == 'social_distance':
            tag_words = social_distance_keywords
        # elif tag == 'all':
        #     tag_words
        #     raise NotImplementedError(tag)
=======
    (
        General, Country, Region, states_subreddit, work_from_home,
        social_distance,
        lock_down,
        social_distance_words, lockdown_words, work_from_home_words,
        covid_words) = get_keywords_collections('reddit')

    tag = running_conditions['tag']

    def _get_tags_words() -> List[str]:
        if tag == 'work_from_home':
            tag_words = work_from_home_words
        elif tag == 'lockdown':
            tag_words = lockdown_words
        elif tag == 'social_distance':
            tag_words = social_distance_words
>>>>>>> fixed .gitignore to remove Output/ and add Example/
        elif tag is None:
            tag_words = []
        else:
            raise NotImplementedError(tag)

        return tag_words

<<<<<<< HEAD
    # OPTIMIZE: figure out how to deal 2 versio of the same thing:
    #    eg work_from_home, work_from_home_words

    tag_words = _get_tags_words()
    subreddit_collection_class: SubredditCollection
    # initial_day_interval = 16
    # HERE erase this initial_day_interval (and automatically load instead)
    initial_day_interval = 1
=======
    subreddit_collection_class: SubredditCollection
    # initial_day_interval = 16
    initial_day_interval = 1  # HERE erase this initial_day_interval (and automatically load instead)
>>>>>>> fixed .gitignore to remove Output/ and add Example/
    frequency = 'day'

    crawler_condition: RedditCrawlerCondition

    def _get_crawler_condition(
            subreddit_collection_class: SubredditCollection) -> RedditCrawlerCondition:
        crawler_condition = {
            'crawler_class': RedditCrawler,
            'collection_class': subreddit_collection_class,
            'initial_interval': initial_day_interval,  # 100
            'request_timestamp': timestamp,
<<<<<<< HEAD
            'respond_type': respond_type,
            'search_type': search_type,
            'frequency': frequency,
            'verbose': True,
            'max_after': max_after
        }
        return crawler_condition

    if collection_name == 'corona_general':

        subreddit_collection_class = {
            'collection': {'subreddit': General, 'aspect': tag, 'query': tag_words},
            'name': collection_name}

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    elif collection_name == 'corona_countries':
        subreddit_collection_class = {
            'collection': {'subreddit': Country,'aspect': tag, 'query': tag_words},
            'name': collection_name}

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    elif collection_name == 'corona_regions':
        subreddit_collection_class = {
            'collection': {'subreddit': Region,'aspect': tag, 'query': tag_words},
            'name': collection_name}

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    elif collection_name == 'corona_states_with_tag':

        assert tag is not None
        tag_words = tag
        # tag_words = tag_words if tag is not None else ALL_KEYWORDS

        subreddit_collection_class = {
            'collection': {'subreddit': states_subreddit,'aspect': tag, 'query': tag_words},
            'name': collection_name}
=======
            'respond_type': running_conditions['respond_type'],
            'search_type': running_conditions['search_type'],
            'frequency': frequency,
            'verbose': True,
            'tag': tag,
        }
        return crawler_condition

    if running_conditions['collection_name'] == 'corona_general':

        subreddit_collection_class = {
            'collection': {'subreddit': General, 'query': _get_tags_words()},
            'name': running_conditions[
                'collection_name']}

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    elif running_conditions['collection_name'] == 'corona_countries':
        subreddit_collection_class = {
            'collection': {'subreddit': Country, 'query': _get_tags_words()},
            'name': running_conditions[
                'collection_name']}

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    elif running_conditions['collection_name'] == 'corona_regions':
        subreddit_collection_class = {
            'collection': {'subreddit': Region, 'query': _get_tags_words()},
            'name': running_conditions[
                'collection_name']}

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    elif running_conditions['collection_name'] == 'work_from_home':
        tag_words = _get_tags_words() if tag is not None else covid_words

        subreddit_collection_class = {
            'collection': {'subreddit': work_from_home, 'query': tag_words},
            'name': running_conditions[
                'collection_name']}

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    # elif running_conditions['collection_name'] == 'lock_down':
    #
    #     subreddit_collection_class = {'collection': {'subreddit': lock_down, 'query': []},
    #                                   'name': running_conditions[
    #                                       'collection_name']}
    #
    #     crawler_condition = _get_crawler_condition(subreddit_collection_class)
    #
    # elif running_conditions['collection_name'] == 'social_distance ':
    #     subreddit_collection_class = {'collection': {'subreddit': social_distance, 'query': []},
    #                                   'name': running_conditions[
    #                                       'collection_name']}
    #
    #     crawler_condition = _get_crawler_condition(subreddit_collection_class)

    elif running_conditions['collection_name'] == 'corona_states_with_tag':
        all_tags = social_distance_words + work_from_home_words + covid_words + lockdown_words
        tag_words = _get_tags_words() if tag is not None else all_tags

        subreddit_collection_class = {
            'collection': {'subreddit': states_subreddit, 'query': tag_words},
            'name': running_conditions[
                'collection_name']}
>>>>>>> fixed .gitignore to remove Output/ and add Example/

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    else:
        raise ValueError('collection_name is not supported')

    return crawler_condition


def select_crawler_condition(
<<<<<<< HEAD
    running_conditions: RunningConditions,
    timestamp: datetime.datetime) -> Tuple[
        Callable, Union[RedditCrawlerCondition, TwitterCrawlerCondition]]:
=======
        running_conditions: RunningConditions,
        timestamp: datetime.datetime) -> Tuple[
    Callable, Union[RedditCrawlerCondition, TwitterCrawlerCondition]]:
>>>>>>> fixed .gitignore to remove Output/ and add Example/
    # timestamp = datetime.datetime.now()

    crawler_conditions: Union[RedditCrawlerCondition, TwitterCrawlerCondition]
    if running_conditions['crawler_option'] == 'reddit':
        crawler_conditions = reddit_crawler_condition(timestamp,
                                                      running_conditions)

        return run_reddit_crawler, crawler_conditions

    elif running_conditions['crawler_option'] == 'twitter':
        crawler_conditions = twitter_crawler_condition(timestamp,
                                                       running_conditions)
        return run_twitter_crawler, crawler_conditions
    else:
        raise ValueError(
            f'selected crawler_class == {running_conditions["crawler_option"]} is not supported')


<<<<<<< HEAD
def get_reddit_running_conditions(max_after: int, tags: Tags, crawler_option: Crawler_type) -> Union[
        List, List[RunningConditionsKeyValue]]:


    def _get_tag_value(tags: Tags) -> Tags:
        if tags is not None:
            _check_reddit_tags_value(tags)

            if len(tags) == 1 and tags[0] == 'all':
                return ALL_REDDIT_TAGS
            else:
                return tags
=======
def get_reddit_running_conditions(tags: Tags) -> Union[
    List, List[RunningConditionsKeyValue]]:
    crawler_option = 'reddit'
    from itertools import product

    def _get_tag_value(tags: Tags):
        if tags is not None:
            _check_reddit_tags_value(tags)
            if len(tags) == 1:
                if tags[0] == 'all':
                    return ALL_REDDIT_TAGS
            return tags
>>>>>>> fixed .gitignore to remove Output/ and add Example/
        else:
            return [tags]

    # --conditions
    tags = _get_tag_value(tags)
<<<<<<< HEAD

    all_collection_name = ALL_REDDIT_COLLECTION_NAMES if tags is None else ALL_REDDIT_COLLECTION_NAMES
    all_search_type = ALL_REDDIT_SEARCH_TYPES
    all_respond_type = ALL_REDDIT_RESPOND_TYPES

    all_running_conditions_key_value: RunningConditionsKeyValue = []

    for max_after, tag, collection_name, search_type, respond_type in product([max_after],
                                                                              tags,
                                                                              all_collection_name,
                                                                              all_search_type,
                                                                              all_respond_type):
        tag_str = tag

        condition_keys: List[Optional[str], int] = [
            max_after, tag_str, collection_name, search_type]

        running_condition: RunningConditions = _get_running_conditions(
            crawler_option, collection_name,
            search_type, respond_type, tag, max_after)
        all_running_conditions_key_value.append(
            (condition_keys, running_condition))

    # # TMP: why do I have the below paragraph here?
    # selected_running_conditions = []
    # for i in all_running_conditions_key_value:
    #     if i[0][1] == 'corona_states_with_tag':
    #         selected_running_conditions.append(i[0])
    # print(selected_running_conditions)

    return all_running_conditions_key_value


def get_twitter_running_conditions(max_after: int, tags: Tags, crawler_option: Crawler_type) -> Union[List, List[RunningConditions]]:

    def _get_tag_value(tags: Tags) -> Tags:
        if tags is not None:
            _check_reddit_tags_value(tags)
            if len(tags) == 1 and tags[0] == 'all':
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

    for max_after, tag, collection_name, search_type, respond_type in product([max_after],
                                                                              tags,
                                                                              all_collection_name,
                                                                              all_search_type,
                                                                              all_respond_type):
        tag_str = tag

        condition_keys: List[Optional[str], int] = [
            max_after, tag_str, collection_name, search_type]

        running_condition: RunningConditions = _get_running_conditions(
            crawler_option, collection_name,
            search_type, respond_type, tag, max_after)
        all_running_conditions_key_value.append(
            (condition_keys, running_condition))

    # # TMP: why do I have the below paragraph here?
    # selected_running_conditions = []
    # for i in all_running_conditions_key_value:
    #     if i[0][1] == 'corona_states_with_tag':
    #         selected_running_conditions.append(i[0])
    # print(selected_running_conditions)
=======
    all_collection_name = ALL_REDDIT_COLLETION_NAMES if tags is None else [
        'corona_general', 'corona_countries',
        'corona_regions', 'corona_states_with_tag']
    all_search_type = ALL_SEARCH_TYPES

    all_running_conditions_key_value: RunningConditionsKeyValue = []

    for tag, collection_name, search_type in product(tags,
                                                     all_collection_name,
                                                     all_search_type):
        tag_str = 'no_tag' if tag is None else tag

        condition_keys: List[str] = [tag_str, collection_name, search_type]

        running_condition: RunningConditions = _get_running_conditions(
            crawler_option, collection_name,
            search_type, tag)
        all_running_conditions_key_value.append(
            (condition_keys, running_condition))

    # all_running_conditions_key_value = [all_running_conditions_key_value[8]]
    #TMP
    selected_running_conditions = []
    for i in all_running_conditions_key_value:
        if i[0][1] == 'corona_states_with_tag':
            selected_running_conditions.append(i[0])
    print(selected_running_conditions)
>>>>>>> fixed .gitignore to remove Output/ and add Example/

    return all_running_conditions_key_value


<<<<<<< HEAD
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


def get_crawler_running_conditions(max_after: int, tags: Tags, crawler_type: Crawler_type) -> Union[List, List[RunningConditions]]:

    if crawler_type == 'reddit':
        return get_reddit_running_conditions(max_after, tags, crawler_type)
    elif crawler_type == 'twitter':
        return get_twitter_running_conditions(max_after, tags, crawler_type)

=======
def get_twitter_running_conditions() -> Union[List, List[RunningConditions]]:
    cralwer_option = 'twitter'

    one_running_conditions: RunningConditions = {
        'crawler_option': cralwer_option,
        'collection_name': 'twitter_tweet',
        'respond_type': 'data_tweet',
        'search_type': 'data_tweet',
        'sort': 'asc'
    }
    two_running_conditions: RunningConditions = {
        'crawler_option': cralwer_option,
        'collection_name': 'twitter_geo',
        'respond_type': 'data_geo',
        'search_type': 'data_geo',
        'sort': 'asc'
    }
    all_running_conditions = []
    all_running_conditions.append(one_running_conditions)
    # all_running_conditions.append(two_running_conditions)

    return all_running_conditions


def get_crawler_running_conditions(tags: Tags, cralwer_type: Crawler_type):
    if cralwer_type == 'reddit':
        return get_reddit_running_conditions(tags)
    elif cralwer_type == 'twitter':
        raise NotImplementedError()
        return get_twitter_running_conditions()
>>>>>>> fixed .gitignore to remove Output/ and add Example/
    else:
        raise ValueError('you must select between reddit or twitter crawler ')


<<<<<<< HEAD
def run_all_reddit_conditions(max_after: int, tags: Tags, timestamp: datetime.datetime, crawler_type: Crawler_type):

    total_returned_data, total_missing_data = 0, 0

    all_running_conditions = get_crawler_running_conditions(
        max_after, tags, crawler_type)
=======

def run_all_reddit_conditions(tags: Tags, timestamp: datetime.datetime, crawler_type: Crawler_type):
    print('>>> start running all reddit conditions... <<<')

    total_returned_data, total_missing_data = 0, 0

    all_running_conditions = get_crawler_running_conditions(tags, crawler_type)
>>>>>>> fixed .gitignore to remove Output/ and add Example/

    # all_running_conditions = all_reddit_running_conditions

    for (i, (condition_keys, running_conditions)) in enumerate(
<<<<<<< HEAD
            all_running_conditions[1:]):
=======
            all_running_conditions):
>>>>>>> fixed .gitignore to remove Output/ and add Example/
        check_running_conditions(running_conditions)

        run_crawler_func, crawler_condition = select_crawler_condition(
            running_conditions=running_conditions, timestamp=timestamp)
        try:
            total_returned_data_per_run, total_missing_data_per_run = run_crawler(
                run_crawler_func, crawler_condition)
            total_returned_data += total_returned_data_per_run
            total_missing_data += total_missing_data_per_run
            print()
        except Exception as e:
            if str(e) not in KNOWN_ERROR:
<<<<<<< HEAD
                print(str(e))
=======

>>>>>>> fixed .gitignore to remove Output/ and add Example/
                raise NotImplementedError(
                    f"unknown error occur in {run_all_conditions.__name__} ")

            else:
                print(f'!!!! The following error occurs = {str(e)} !!!')
                condition_keys_str: str = ','.join(condition_keys)

                if i == len(all_running_conditions) - 1:
                    print(
                        f' || skip the the current condition = ({condition_keys_str}) ==> No more running conditions to run ==> exiting {run_all_conditions.__name__}()')
                    print()
                else:
                    next_condition_keys = all_running_conditions[i + 1][0]
<<<<<<< HEAD
                    next_condition_keys_str: str = ','.join(
                        next_condition_keys)
                    print(
                        f' || skip the the current condition = ({condition_keys_str}) ==> start next running condition = {next_condition_keys_str} ')
                    print()
    #
=======
                    next_condition_keys_str: str = ','.join(next_condition_keys)
                    print(
                        f' || skip the the current condition = ({condition_keys_str}) ==> start next running condition = {next_condition_keys_str} ')
                    print()

>>>>>>> fixed .gitignore to remove Output/ and add Example/
    print(
        f" || total_returned_data = {total_returned_data} || total_missing_data = {total_missing_data}")


<<<<<<< HEAD
def run_all_twitter_conditions(max_after: int, tags: Tags, timestamp: datetime.datetime,
                               crawler_type: Crawler_type):

    total_returned_data, _ = 0, 0

    all_running_conditions = get_crawler_running_conditions(max_after,
                                                            tags,
                                                            crawler_type)

    for (i, (condition_keys, running_conditions)) in enumerate(
            all_running_conditions):
        check_running_conditions(running_conditions)

        run_crawler_func, crawler_condition = select_crawler_condition(
            running_conditions=running_conditions, timestamp=timestamp)

        try:

            total_returned_data_per_run = run_crawler(
                run_crawler_func, crawler_condition)
            total_returned_data += total_returned_data_per_run
            print()
        except Exception as e:
            if str(e) not in KNOWN_ERROR:

                raise NotImplementedError(
                    f"unknown error occur in {run_all_conditions.__name__} ")

            else:
                print(
                    f'!!!! The following error occurs = {str(e)} in {run_all_conditions.__name__}!!!')

    print(
        f" || total_returned_data = {total_returned_data}")


def run_all_conditions(max_after: int, tags: Tags, crawler_type: Crawler_type):
    timestamp = datetime.datetime.now()
    print(f'>>> start running all {crawler_type} conditions... <<<')
    if crawler_type == 'reddit':
        run_all_reddit_conditions(max_after, tags, timestamp, crawler_type)
    elif crawler_type == 'twitter':
        run_all_twitter_conditions(max_after, tags, timestamp, crawler_type)
    else:
        raise ValueError('your selected crawler_type is not implementd')
=======


def run_all_conditions(tags: Tags, crawler_type: Crawler_type):
    timestamp = datetime.datetime.now()
    run_all_reddit_conditions(tags, timestamp, crawler_type)
    # run_all_twitter_conditions(tags)
>>>>>>> fixed .gitignore to remove Output/ and add Example/


@click.command()
@click.option('--select_all_conditions/--select_one_condition', default=False)
# NOTE: default is set to tuple() when multiple=True, regardless of default set to None
@click.option('--tags', multiple=True, type=click.STRING)
<<<<<<< HEAD
@click.option('--max_after', type=int, default=MAX_AFTER)
@click.option('--crawler_type',  type=click.Choice(['reddit', 'twitter']))
# @click.argument('tags', nargs=-1)
@my_timer
def main(select_all_conditions: bool, tags: Tags, max_after: int, crawler_type: str) -> None:
    tags = None if len(tags) == 0 else tags
    if select_all_conditions:
        run_all_conditions(max_after, tags, crawler_type)
=======
@click.option('--crawler_type',  type=click.Choice(['reddit', 'twitter']))
# @click.argument('tags', nargs=-1)
@my_timer
def main(select_all_conditions: bool, tags: Tags, crawler_type: str) -> None:
    tags = None if len(tags) == 0 else tags
    if select_all_conditions:
        run_all_conditions(tags, crawler_type)
>>>>>>> fixed .gitignore to remove Output/ and add Example/
    else:
        raise NotImplementedError
        # run_selected_condition() # TODO can click command activate when I call the function only? click.invoke?

    print(f">>>> exit program <<<<<")

    # TODO
    #   : add query into metadata
    #   : in prepare, make sure that after are in syng iwth max_after and frequency
    #   : check corona_states_with_tag/comment => responds is almost 20,000
    #   : work_from_home/comment/data => no lastest folder
    #   : remove the following variables
    #       in crawler_conditions
    #           >> initial_day_interal (code already created so that the appropriate range are collected)
    #           >> frequency (code already adjust this automatically)
    #   : learn about click (30 mins)
    #       >> add the following option
    #           :request_with_tag (boolean)
    #           :max_interval (int) = max range interval to be retrieved
    #           :run_all_cases (boolean) = if true run all test if false => you must specficy
    #               RunningCondition
    #                 crawler_option,
    #                 collection_name,
    #                 respond_type ?
    #                 search_type (str) = ['data']
    #                 sort
    #                 verbose (boolean)
    #                 frequency
    #       >> convert check_running_conditions to
    #   : check that chech_all_conditions are align with the new code (implemented with click)
    #   : add tags option for Reddit (separate folder by tags: work_from_home/... or covid/... or )
    #       > for without_tag_class option => state_with_tags includes all tags. (not just 1 type)
    #       > change folder name to reflect the changes (with_tag_class / without_tag_class)
    #   : change twitter to output total_returned_data_per_run and total_missing_data_per_run
    #   : checking key value
    #       > for twitter convert to appropriate key
    #   : finished adding sentiment analysis for Twitter
    #   : test that RedditCrawler works as expect
    #   :write script to run program every day. (get new info everyday)
    #  :test the following cases
    #       >create class template that can used by twitter too
    #       > use twitterscraper as base api to scarp
    #           > is it allowed for keyword search?
    #           > is it allowed for hashtags? (or hashtags is already done by keyword search?)
    #           > is the output sorted?
    #           > scalping for each month. (


if __name__ == '__main__':
    main()
<<<<<<< HEAD


=======
>>>>>>> fixed .gitignore to remove Output/ and add Example/
