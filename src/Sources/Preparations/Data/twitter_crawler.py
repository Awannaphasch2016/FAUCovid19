#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Prepare and crawl twitter data"""

import datetime
import json
import time
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type

import GetOldTweets3 as got  # type: ignore
from typing_extensions import TypedDict
from src.Sources.Preparations.Features.sentiment_analysis import get_sentiment

from Tests.check_conditions import check_response_keys
from src.Utilities import get_saved_file_path
from src.Utilities import my_timer
from src.Utilities import save_to_file
from src.Utilities import Frequency
from src.Utilities import Json
from src.Utilities import TwitterAggs
from src.Utilities import TwitterCollection
from src.Utilities import TwitterData
from src.Utilities import TwitterMetadata
from src.Utilities import TwitterRunningConstraints
from src.Utilities import Url
from src.Utilities import Tags
from src.Utilities import Query
from src.Utilities import epoch_datetime
from src.Utilities import ensure_epoch_datetime
from src.Utilities import only_download_full_day
# from Utilities.ensure_type import ensure_json
from global_parameters import BASE_DIR
from global_parameters import MAX_AFTER


# Json = Dict


class TwitterCrawler(object):
    """
    This class will prepare and crawl data from twitter
    """

    def __init__(self,
                 twitter_collection_class: TwitterCollection,
                 respond_type: str,
                 search_type: str,
                 frequency: Frequency,
                #  aspect: str,
                 verbose: int,
                 ):

        self.crawler_name = 'TwitterCrawler'
        self.verbose = verbose
        self.prepare_crawler(twitter_collection_class,
                             respond_type,
                             search_type,
                             frequency,
                            #  aspect,
                             )

    def prepare_crawler(self,
                        twitter_collection_class: TwitterCollection,
                        respond_type: str,
                        search_type: str,
                        frequency: Frequency,
                        # aspect: str,
                        ):
        """
        prepare common data that will be used among class's methods

        :type twitter_collection_class: TwitterCollection
        :param twitter_collection_class: Dict contains info about collection of data that will be crawled

        :type respond_type: str
        :param respond_type: desired respond type by crawler

        :type search_type: str
        :param search_type: desired search type by crawler

        :type frequency: Frequency
        :param frequency: interval of time to retrieved data

        :return:
        """
        self.respond_type = respond_type
        self.search_type = search_type
        self.frequency = frequency
        self.collection_name = twitter_collection_class['name']
        self.collection = twitter_collection_class['collection']

        # self.aspect = aspect 
        self.aspect = self.collection['aspect'] 
        self.query = self.collection['query']


    def get_geo_data(self,
                     running_constraints: TwitterRunningConstraints,
                     res: Json) -> Dict:
        raise NotImplementedError

    def get_tweet_data(self,
                       running_constraints: TwitterRunningConstraints,
                       res: Json) -> Json:
        """
        get tweet data

        :type running_constraints: TwitterRunningConstraints
        :param running_constraints: Dict contains keys that determines contains before running a crolwer

        :type res: Json
        :param res: respond from (ANY) twitter api

        :rtype: Json
        :return: respond data with appropriate respond key format
        """

        res = _get_twitter_data(res, running_constraints, self)
        res = _get_twitter_aggs(res, running_constraints, self)
        res = _get_twitter_metadata(res, running_constraints, self, self.aspect, self.query)

        check_response_keys(res)

        return res

    def apply_crawling_strategy(self,
                                running_constraints: TwitterRunningConstraints,
                                res: Optional[Json]) -> Dict:
        """
        apply crawler "strategy" where a strategy is determined by selected collection type

        :type running_constraints: TwitterRunningConstraints
        :param running_constraints: Dict contains keys that determines contains before running a crolwer

        :type res: Json
        :param res: respond from (ANY) twitter api

        :rtype: Dict
        :return: respond data with appropriate respond key format
        """

        if self.respond_type == 'data_geo':
            return self.get_geo_data(running_constraints,
                                     res)
        elif self.respond_type == 'data_tweet':
            return self.get_tweet_data(running_constraints,
                                       res)
        else:
            raise ValueError('')

    def get_response(self):
        raise NotImplementedError('')
        pass

    def get_url(self, running_constraints: TwitterRunningConstraints) -> Url:
        raise NotImplementedError

    @my_timer
    # @signature_logger
    def get_responds(self,
                     running_constraints: TwitterRunningConstraints) -> Optional[Json]:
        """
        prepare varaibles to be pass in (ANY) api and prepare output from (ANY) api

        :type running_constraints: TwitterRunningConstraints
        :param running_constraints: Dict contains keys that determines contains before running a crolwer

        :rtype: None or Json
        :return: respond data with appropriate respond key format
        """

        after = running_constraints['after']
        before = running_constraints['before']
        # after = 3
        # before = 2
        size = running_constraints['size']
        fields = running_constraints['fields']
        sort = running_constraints['sort']

        only_download_full_day(self.frequency, before, after)

        date_since = str(self.time_since) 
        date_until = str(self.time_until)

        # NOTE: chain multiple vocab with AND or OR
        # query = ' AND '.join(self.collection) if len(
        #     self.collection) > 0 else self.collection
        query = ' OR '.join(self.collection) if len(
            self.collection) > 0 else self.collection

        if size is None:
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query) \
                .setSince(date_since) \
                .setUntil(date_until) \
                .setLang('en')

        else:
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query) \
                .setSince(date_since) \
                .setUntil(date_until) \
                .setMaxTweets(size) \
                .setLang('en')

        s = time.time()
        # res = got.manager.TweetManager.getTweets(tweetCriteria,debug=True)
        res = got.manager.TweetManager.getTweets(tweetCriteria)
        # print(res)
        f = time.time()
        self.total_request_time_in_milli_second = (f - s) * 1000

        return res

    def run(self,
            before: Optional[int],
            after: int
            ) -> Optional[Tuple[Dict[str, Dict], int]]:
        """
        crawl ALL data by running all iteration (loops) neccessary to retrieved all data. (this could largely depends on how selected twitter api are designed))

        :type before: None or int
        :param before: date in which all aata BEFORE this date should be retrieved

        :type after: int
        :param after: date in which all aata AFTER this date should be retrieved

        :rtype: None or tuple of dict and int
        :return: all respond (crawled) data with appropriate respond key format
        """

        try:

            responds_content = self.run_once(before, after)

            if responds_content is None:
                return
            else:
                total_result = responds_content['metadata']['total_results']
                if self.verbose:
                    print(
                        f" {self.current_condition_str} || total_results = {total_result}")

        # missing_results = responds_content['metadata']['size'] - total_result # next fix argument before I fie this
        # missing_results = 0 if np.sign(
        #     missing_results) > 0 else missing_results
        # if self.verbose:
        #     print(
        #         f" {self.current_condition_str} || total_results = {total_result} || missing_result = {missing_results}")
        # else:
        #     print(f'missing_reulst = {missing_results}')

        except Exception as e:
            if str(e) != 'responds are empty':
                print(e)
                raise NotImplementedError(
                    f"exception occur in {self.run.__name__}")
            else:
                raise Warning(str(e))

        return responds_content, total_result

    @my_timer
    def run_once(self,
                 before: int,
                 after: int
                 ) -> Optional[Dict]:
        """
        crawl 1 iteration (loops) neccessary to retrieved all data.

        :type before: None or int
        :param before: date in which all aata BEFORE this date should be retrieved

        :type after: int
        :param after: date in which all aata AFTER this date should be retrieved

        :rtype: None or Dict
        :return: respond (crawled) data for 1 iteration with appropriate respond key format
        """

        running_constraints = self.prepare_running_crawler(before, after)

        res = self.get_responds(running_constraints)
        if res is None:
            return
        else:
            reponds_content = self.apply_crawling_strategy(running_constraints,
                                                           res)
        return reponds_content

    def get_submission_avg_per_day(self, responds_content):
        raise NotImplementedError
        pass

    def adjust_after_step(self, per_day_average, max_responds_size):
        raise NotImplementedError
        pass

    def prepare_running_crawler(self,
                                before: int,
                                after: int) -> TwitterRunningConstraints:
        """
        prepare dict constraints that will be used to run (crawl) data for each iteration

        :type before: None or int
        :param before: date in which all aata BEFORE this date should be retrieved

        :type after: int
        :param after: date in which all aata AFTER this date should be retrieved

        :rtype:  TwitterRunningConstraints
        :return: dict of constraint that will be used to run (crawl) data
        """

        running_constraints: TwitterRunningConstraints

        running_constraints = {
            'before': before,
            'after': after,
            'aggs': 'created_utc',
            'size': None,
            'metadata': 'true',
            'sort': 'asc',
            'fields': None,
        }

        if self.frequency == 'day':
            self.time_since = datetime.datetime.now().date() - datetime.timedelta(
                days=after)
            self.time_until = datetime.datetime.now().date() - datetime.timedelta(
                days=before)
        else:
            raise NotImplementedError

        self.current_condition_str = f'aspect = {self.aspect} -> query = {self.query} || collection_name = {self.collection_name} || search_type = {self.search_type} || respond_type = {self.respond_type}' \
                                     f'|| frequency = {self.frequency} || {after} <= x < {before} || {str(self.time_since)} to {str(self.time_until)}'

        if self.verbose:
            print(
                f" {self.current_condition_str}")

        return running_constraints

    def after_run(self):
        raise NotImplementedError


# NOTE: In constrast to TwitterCrawlerCondition, RedditCrawlerCondition need aspect because aspect is used to group 'subreddit' into collection to reflect aspect sentiment
class TwitterCrawlerCondition(TypedDict):
    crawler_class: Type[TwitterCrawler]
    collection_class: TwitterCollection
    interval: int
    request_timestamp: datetime.datetime
    respond_type: str
    search_type: str
    frequency: str
    aspect: Optional[str]
    max_after: int


def run_twitter_crawler(
        twitter_crawler_condition: TwitterCrawlerCondition) -> List[int]:
    """
    prepared varaibles, check conditions, run crawlers and saved respond data.

    :type twitter_crawler_condition: TwitterCrawlerCondition
    :param twitter_crawler_condition: shared conditions (constraints) not specific to any given crawler

    :return: list of int
    :return: total number of returned responds data
    """

    def print_twitter_cralwer_condition():
        print('twitter_crawler_condition = ')
        for i, j in twitter_crawler_condition.items():
            print(f'    {i}: {j}')

    print_twitter_cralwer_condition()

    total_returned_data = 0

    crawler_class: Type[TwitterCrawler] = twitter_crawler_condition[
        'crawler_class']
    twitter_collection_class = twitter_crawler_condition['collection_class']
    interval = twitter_crawler_condition['interval']
    request_timestamp = twitter_crawler_condition['request_timestamp']
    respond_type = twitter_crawler_condition['respond_type']
    search_type = twitter_crawler_condition['search_type']
    frequency = twitter_crawler_condition['frequency']
    max_after = twitter_crawler_condition['max_after']
    # aspect = twitter_crawler_condition['collection_class']['collection']['aspect']

    if frequency == 'day':
        interval_collection: List[int] = [days_to_subtract for days_to_subtract
                                          in list(range(max_after))[::interval]]
    else:
        raise NotImplementedError('')

    interval_range = list(
        zip(interval_collection[:-1], interval_collection[1:]))[::-1]
    # interval_range = list(
    #     zip(interval_collection[:-1], interval_collection[1:]))

    for ind, (before, after) in enumerate(interval_range[:3]):
        twitter_crawler = crawler_class(
            twitter_collection_class=twitter_collection_class,
            respond_type=respond_type,
            search_type=search_type,
            frequency=frequency,
            # aspect=aspect,
            verbose=True)

        print(f" || day interval = {interval}")

        try:

            returned_data_from_twitter_run = twitter_crawler.run(before, after)

            if returned_data_from_twitter_run is None:
                break
            else:
                responds_content, num_returned_data = returned_data_from_twitter_run
                saved_file = get_saved_file_path(twitter_crawler.time_since, twitter_crawler.time_until,
                                                 path_name=BASE_DIR / f'Outputs/Data/{twitter_crawler.crawler_name}/{twitter_crawler.aspect}/{twitter_crawler.collection_name}/{twitter_crawler.search_type}/{twitter_crawler.respond_type}')
                save_to_file(responds_content,
                             saved_file)
                print('')
        except Exception as e:
            if str(e) != 'responds are empty':
                print(e)
                raise NotImplementedError(
                    f"unknown error occur in {run_twitter_crawler.__name__} ")
    print(
        f'|| total returned data = {total_returned_data}')
    print(' >>>> finished crawling data <<<<')
    print()
    return total_returned_data


# =====================
# == Test Twitter
# =====================


class doc_count_per_frequency(TypedDict):
    doc_count: int
    key: epoch_datetime


class aggs_dict(TypedDict):
    created_utc: List[doc_count_per_frequency]


def _get_twitter_data(res: Json,
                      running_constraints: TwitterRunningConstraints,
                      crawler_instance: TwitterCrawler) -> Json:
    """
    FIXME: this function should be method of TwitterCrawler class. (Is there any reason not to?)
    prepare and format 'data' key in respond data to have an appropriate format

    :type respond_type: str
    :param respond_type: desired respond type by crawler

    :type running_constraints: TwitterRunningConstraints
    :param running_constraints: Dict contains keys that determines contains before running a crolwer

    :type crawler_instance: TwitterCrawler
    :param crawler_instance: twitter crawler class

    :rtype: Json
    :return: respond data with appropriate 'data' key format
    """

    def convert_tweets_to_dict(x): return vars(x)

    def ensure_json(res: Dict) -> Json:
        r = json.dumps(res)
        loaded_r = json.loads(r)
        return loaded_r

    res_data: List[TwitterData]
    res_data = []
    for tweet in res:
        res = convert_tweets_to_dict(tweet)
        res['date'] = ensure_epoch_datetime(res['date'])
        res = ensure_json(res)
        res_data.append(res)

    res_data_dict = ensure_json({'data': res_data})

    def standardize_responses_key_name():
        # FIXME: convert responses key for twitter and reddit to have the same key name and use case
        pass

    def check_responses_consistency(res: Json) -> None:

        if len(res['data']) > 0:
            for i in range(len(res['data'])):
                pass
        else:
            raise Warning('responds are empty')
    
    @my_timer
    def _get_sentiment(x) -> float:

        text: Optional[str]

        text = x['text']
        if text is None or len(text) == 0:
            return 0.0
        else:
            sentiment_polarity = get_sentiment(text)
            return sentiment_polarity

    check_responses_consistency(res_data_dict)

    from tqdm import tqdm
    all_data_with_sentiment = []
    for data in tqdm(res_data_dict['data']):
        data_with_sentiment = data
        data_with_sentiment['sentiment'] = _get_sentiment(data)
        all_data_with_sentiment.append(data_with_sentiment)
        # data['sentiment'] = _get_sentiment(data)

    res_data_dict['data'] = all_data_with_sentiment



    return res_data_dict


def _get_twitter_aggs(res: Json,
                      running_constraints: TwitterRunningConstraints,
                      crawler_instance: TwitterCrawler,
                      ) -> Json:
    """
    FIXME: this function should be method of TwitterCrawler class. (Is there any reason not to?)
    prepare and format 'aggs' key in respond data to have an appropriate format

    :type respond_type: str
    :param respond_type: desired respond type by crawler

    :type running_constraints: TwitterRunningConstraints
    :param running_constraints: Dict contains keys that determines contains before running a crolwer

    :type crawler_instance: TwitterCrawler
    :param crawler_instance: twitter crawler class

    :rtype: Json
    :return: respond data with appropriate 'aggs' key format
    """

    aggs_dict: TwitterAggs

    if 'aggs' not in res:
        def aggs_doc_count_per_frequency() -> doc_count_per_frequency:
            x: Dict[str, int]
            x = {}
            counter = {}
            doc_count_dict = {}
            get_date_datetime_from_epoch_datetime = lambda \
                x: datetime.datetime.fromtimestamp(x).date()

            def convert_datetime_to_epoch_datetime(x): return \
                str(datetime.datetime(x.year, x.month,
                                      x.day).timestamp()).split(
                    '.')[0]
            for i in res['data']:
                date_from_datetime = get_date_datetime_from_epoch_datetime(
                    i['date'])
                date_epoch_datetime = convert_datetime_to_epoch_datetime(
                    date_from_datetime)
                assert len(date_epoch_datetime) == 10, ''

                if date_epoch_datetime not in counter:
                    counter[date_epoch_datetime] = 0
                else:
                    counter[date_epoch_datetime] += 1

            for utc, count in counter.items():
                doc_count_dict['doc_count'] = count
                doc_count_dict['key'] = utc

            return doc_count_dict

        res['aggs'] = {'created': aggs_doc_count_per_frequency()}

        return res
    else:
        raise NotImplementedError()


def _get_twitter_metadata(res: Json,
                          running_constraints: TwitterRunningConstraints,
                          crawler_instance: TwitterCrawler,
                          aspect: Tags,
                          query: Query,
                          ) -> Json:
    """
    FIXME: this function should be method of TwitterCrawler class. (Is there any reason not to?)
    prepare and format 'metadata' key in respond data to have an appropriate format

    :type respond_type: str
    :param respond_type: desired respond type by crawler

    :type running_constraints: TwitterRunningConstraints
    :param running_constraints: Dict contains keys that determines contains before running a crolwer

    :type crawler_instance: TwitterCrawler
    :param crawler_instance: twitter crawler class

    :type aspect: Tags
    :param aspect: any specified aspect

    :type query: Query
    :param query: list of words assigned for a selected aspect

    :rtype: Json
    :return: respond data with appropriate 'metadata' key format
    """

    after = running_constraints['after']
    before = running_constraints['before']
    size = running_constraints['size']
    sort = running_constraints['sort']
    fields = running_constraints['fields']

    keys = ['running_constraints', 'after', 'aggs', 'before',
            'execution_time_milliseconds', 'frequency', 'index',
            'results_returned', 'size', 'sort', 'timed_out',
            'search_words', 'total_results', 'fields', 'aspect',  'query']

    def create_metadata() -> TwitterMetadata:
        x = {'running_constraints': running_constraints,
             'after': after,
             'before': before,
             'aggs': list(res['aggs'].keys()),
             'execution_time_milliseconds': crawler_instance.total_request_time_in_milli_second,
             'frequency': crawler_instance.frequency,
             'size': size,
             'sort': sort,
             'search_words': crawler_instance.collection,
             'total_results': len(res['data']),
             'fields': fields,
             'aspect': aspect,
             'query': query,
             'results_returned': None,
             'timed_out': None,
             'index': None,
             }

        assert len(set(list(x.keys())) ^ set(keys)) == 0

        return x

    if 'metadata' not in res:
        aggs_dict: TwitterAggs
        res['metadata'] = create_metadata()

        return res
    else:
        # NOTE: why do I need else section here? can't I just add metadata to the data? 
        assert len(res['metadata']) == len(keys), ''

        for i in keys:
            if i not in res['metadata']:
                raise ValueError('')
