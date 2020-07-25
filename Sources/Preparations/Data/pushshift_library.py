import sys


sys.path.append("C:/Users/Anak/PycharmProjects/Covid19CookieCutter")
sys.path.append("C:/Users/Anak/PycharmProjects/Covid19CookieCutter/Sources")

from global_parameters import ALL_TWITTER_KEYWORDS

import datetime
from Utilities.declared_typing import Crawler_type
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
from global_parameters import ALL_REDDIT_COLLETION_NAMES
from global_parameters import ALL_REDDIT_TAGS
from global_parameters import ALL_REDDIT_SEARCH_TYPES
from global_parameters import KNOWN_ERROR


def _get_running_conditions(crawler_option: str,
                            collection_name: str,
                            search_type: str,
                            tag: Optional[str]
                            ) -> RunningConditions:
    running_conditions_dict: RunningConditions = {
        'crawler_option': crawler_option,
        'collection_name': collection_name,
        'respond_type': 'data',
        'search_type': search_type,
        'sort': 'asc',
        'tag': tag
    }
    return running_conditions_dict


def run_crawler(run_crawler_func: Callable, crawler_condition: Union[
    RedditCrawlerCondition, TwitterCrawlerCondition],
                ) -> Tuple[int, int]:
    return run_crawler_func(crawler_condition)


def get_keywords_collections(crawler_type: str):
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

    elif crawler_type == 'twitter':
        # coronavirus, #coronavirusoutbreak, #coronavirusPandemic, #covid19, #covid_19, #epitwitter, #ihavecorona
        hashtags = ['#coronavirus', '#coronavirusoutbreak',
                    '#coronavirusPandemic', '#covid19', '#covid_19',
                    '#epitwitter', '#ihavecorona']
        # corona_keywords = ['corona', 'covid']
        # corona_keywords = ALL_TWITTER_KEYWORDS
        corona_keywords = ['Covid']
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


def twitter_crawler_condition(
        timestamp: datetime.datetime,
        running_conditions: RunningConditions) -> TwitterCrawlerCondition:
    hashtags, corona_keywords, state_keywords = get_keywords_collections(
        'twitter')

    day_interval: int = 1
    frequency: Frequency = 'day'

    if running_conditions['collection_name'] == 'twitter_tweet':
        twitter_crawler_collection: TwitterCollection = {
            'collection': corona_keywords,
            'name':
                running_conditions[
                    'collection_name']}

        crawler_condition: TwitterCrawlerCondition = {
            'crawler_class': TwitterCrawler,
            'collection_class': twitter_crawler_collection,
            'interval': day_interval,
            'request_timestamp': timestamp,
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

        crawler_condition: TwitterCrawlerCondition = {
            'crawler_class': TwitterCrawler,
            'collection_class': twitter_crawler_collection,
            'interval': day_interval,
            'request_timestamp': timestamp,
            'respond_type': running_conditions['respond_type'],
            'search_type': running_conditions['search_type'],
            'frequency': frequency
        }
    else:
        raise NotImplementedError()

    return crawler_condition


def reddit_crawler_condition(
        timestamp: datetime.datetime,
        running_conditions: RunningConditions) -> RedditCrawlerCondition:
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
        elif tag is None:
            tag_words = []
        else:
            raise NotImplementedError(tag)

        return tag_words

    subreddit_collection_class: SubredditCollection
    # initial_day_interval = 16
    initial_day_interval = 1  # HERE erase this initial_day_interval (and automatically load instead)
    frequency = 'day'

    crawler_condition: RedditCrawlerCondition

    def _get_crawler_condition(
            subreddit_collection_class: SubredditCollection) -> RedditCrawlerCondition:
        crawler_condition = {
            'crawler_class': RedditCrawler,
            'collection_class': subreddit_collection_class,
            'initial_interval': initial_day_interval,  # 100
            'request_timestamp': timestamp,
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

        crawler_condition = _get_crawler_condition(subreddit_collection_class)

    else:
        raise ValueError('collection_name is not supported')

    return crawler_condition


def select_crawler_condition(
        running_conditions: RunningConditions,
        timestamp: datetime.datetime) -> Tuple[
    Callable, Union[RedditCrawlerCondition, TwitterCrawlerCondition]]:
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


def get_reddit_running_conditions(tags: Tags, crawler_option: Crawler_type) -> Union[
    List, List[RunningConditionsKeyValue]]:

    from itertools import product

    def _get_tag_value(tags: Tags):
        if tags is not None:
            _check_reddit_tags_value(tags)
            if len(tags) == 1:
                if tags[0] == 'all':
                    return ALL_REDDIT_TAGS
            return tags
        else:
            return [tags]

    # --conditions
    tags = _get_tag_value(tags)
    all_collection_name = ALL_REDDIT_COLLETION_NAMES if tags is None else [
        'corona_general', 'corona_countries',
        'corona_regions', 'corona_states_with_tag']
    all_search_type = ALL_REDDIT_SEARCH_TYPES

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
    #TMP why do I have the below paragraph here?
    selected_running_conditions = []
    for i in all_running_conditions_key_value:
        if i[0][1] == 'corona_states_with_tag':
            selected_running_conditions.append(i[0])
    print(selected_running_conditions)

    return all_running_conditions_key_value


def get_twitter_running_conditions(tags: Tags,crawler_option: Crawler_type) -> Union[List, List[RunningConditions]]:

    one_running_conditions: RunningConditions = {
        'crawler_option': crawler_option,
        'collection_name': 'twitter_tweet',
        'respond_type': 'data_tweet',
        'search_type': 'data_tweet',
        'sort': 'asc',
        'tag': tags,
    }
    two_running_conditions: RunningConditions = {
        'crawler_option': crawler_option,
        'collection_name': 'twitter_geo',
        'respond_type': 'data_geo',
        'search_type': 'data_geo',
        'sort': 'asc',
        'tag': tags
    }

    all_running_conditions = []
    all_running_conditions.append(one_running_conditions)
    # all_running_conditions.append(two_running_conditions)

    tmp = []
    for i in all_running_conditions:
        tag = i['tag']
        collection_name = i['collection_name']
        search_type = i['search_type']
        tmp.append(([tag, collection_name, search_type], i))
    all_running_conditions = tmp

    return all_running_conditions


def get_crawler_running_conditions(tags: Tags, crawler_type: Crawler_type):

    if crawler_type == 'reddit':
        return get_reddit_running_conditions(tags, crawler_type)
    elif crawler_type == 'twitter':
        return get_twitter_running_conditions(tags, crawler_type)
    else:
        raise ValueError('you must select between reddit or twitter crawler ')



def run_all_reddit_conditions(tags: Tags, timestamp: datetime.datetime, crawler_type: Crawler_type):

    total_returned_data, total_missing_data = 0, 0

    all_running_conditions = get_crawler_running_conditions(tags, crawler_type)

    # all_running_conditions = all_reddit_running_conditions

    for (i, (condition_keys, running_conditions)) in enumerate(
            all_running_conditions):
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
                    next_condition_keys_str: str = ','.join(next_condition_keys)
                    print(
                        f' || skip the the current condition = ({condition_keys_str}) ==> start next running condition = {next_condition_keys_str} ')
                    print()

    print(
        f" || total_returned_data = {total_returned_data} || total_missing_data = {total_missing_data}")


def run_all_twitter_conditions(tags: Tags, timestamp: datetime.datetime,
                                  crawler_type: Crawler_type):

    total_returned_data, _ = 0, 0

    all_running_conditions = get_crawler_running_conditions(tags,
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
                print(f'!!!! The following error occurs = {str(e)} in {run_all_conditions.__name__}!!!')

    print(
        f" || total_returned_data = {total_returned_data}")


def run_all_conditions(tags: Tags, crawler_type: Crawler_type):
    timestamp = datetime.datetime.now()
    print(f'>>> start running all {crawler_type} conditions... <<<')
    if crawler_type == 'reddit':
        run_all_reddit_conditions(tags, timestamp, crawler_type)
    elif crawler_type == 'twitter':
        run_all_twitter_conditions(tags, timestamp, crawler_type)
    else:
        raise ValueError('your selected crawler_type is not implementd')


@click.command()
@click.option('--select_all_conditions/--select_one_condition', default=False)
# NOTE: default is set to tuple() when multiple=True, regardless of default set to None
@click.option('--tags', multiple=True, type=click.STRING)
@click.option('--crawler_type',  type=click.Choice(['reddit', 'twitter']))
# @click.argument('tags', nargs=-1)
@my_timer
def main(select_all_conditions: bool, tags: Tags, crawler_type: str) -> None:
    tags = None if len(tags) == 0 else tags
    if select_all_conditions:
        run_all_conditions(tags, crawler_type)
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
