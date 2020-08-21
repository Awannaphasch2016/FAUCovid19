import datetime
import json
import time
from typing import Dict
from typing import List
from typing import Optional
<<<<<<< HEAD
from typing import Tuple
=======
>>>>>>> fixed .gitignore to remove Output/ and add Example/
from typing import Type

import GetOldTweets3 as got  # type: ignore
from typing_extensions import TypedDict
<<<<<<< HEAD
from Sources.Preparations.Features.sentiment_analysis import get_sentiment

from Test_dir.test_conditions import check_response_keys
from Utilities import get_saved_file_path
from Utilities import my_timer
from Utilities import save_to_file
=======

from Utilities import get_saved_file_path
from Utilities import my_timer
from Utilities import save_to_file
from Test_dir.test_conditions import check_response_keys
>>>>>>> fixed .gitignore to remove Output/ and add Example/
from Utilities.declared_typing import Frequency
from Utilities.declared_typing import Json
from Utilities.declared_typing import TwitterAggs
from Utilities.declared_typing import TwitterCollection
from Utilities.declared_typing import TwitterData
from Utilities.declared_typing import TwitterMetadata
from Utilities.declared_typing import TwitterRunningConstraints
from Utilities.declared_typing import Url
<<<<<<< HEAD
from Utilities.declared_typing import Tags
from Utilities.declared_typing import Query
from Utilities.declared_typing import epoch_datetime
from Utilities.ensure_type import ensure_epoch_datetime
from Utilities.ensure_type import only_download_full_day
# from Utilities.ensure_type import ensure_json
from global_parameters import BASE_DIR
from global_parameters import MAX_AFTER
=======
from Utilities.declared_typing import epoch_datetime
from Utilities.ensure_type import ensure_epoch_datetime
# from Utilities.ensure_type import ensure_json
from global_parameters import BASE_DIR
>>>>>>> fixed .gitignore to remove Output/ and add Example/


# Json = Dict


class TwitterCrawler(object):
    def __init__(self,
                 twitter_collection_class: TwitterCollection,
                 respond_type: str,
                 search_type: str,
                 frequency: Frequency,
<<<<<<< HEAD
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
=======
                 verbose: int):

        self.crawler_name = 'TwitterCrawler'
        self.verbose = verbose
        self.prepare_crawler(twitter_collection_class, respond_type,
                             search_type, frequency)
>>>>>>> fixed .gitignore to remove Output/ and add Example/

    def prepare_crawler(self,
                        twitter_collection_class: TwitterCollection,
                        respond_type: str,
                        search_type: str,
<<<<<<< HEAD
                        frequency: Frequency,
                        # aspect: str,
                        ):
=======
                        frequency: Frequency):
>>>>>>> fixed .gitignore to remove Output/ and add Example/
        self.respond_type = respond_type
        self.search_type = search_type
        self.frequency = frequency
        self.collection_name = twitter_collection_class['name']
        self.collection = twitter_collection_class['collection']

<<<<<<< HEAD
        # self.aspect = aspect 
        self.aspect = self.collection['aspect'] 
        self.query = self.collection['query']


=======
>>>>>>> fixed .gitignore to remove Output/ and add Example/
    def get_geo_data(self,
                     running_constraints: TwitterRunningConstraints,
                     res: Json) -> Dict:
        raise NotImplementedError

    def get_tweet_data(self,
                       running_constraints: TwitterRunningConstraints,
                       res: Json) -> Json:

        res = _get_twitter_data(res, running_constraints, self)
        res = _get_twitter_aggs(res, running_constraints, self)
<<<<<<< HEAD
        res = _get_twitter_metadata(res, running_constraints, self, self.aspect, self.query)
=======
        res = _get_twitter_metadata(res, running_constraints, self)
>>>>>>> fixed .gitignore to remove Output/ and add Example/

        check_response_keys(res)

        return res

    def apply_crawling_strategy(self,
                                running_constraints: TwitterRunningConstraints,
<<<<<<< HEAD
                                res: Optional[Json]) -> Dict:
=======
                                res: Json) -> Dict:
>>>>>>> fixed .gitignore to remove Output/ and add Example/

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
<<<<<<< HEAD
                     running_constraints: TwitterRunningConstraints) -> Optional[Json]:

        after = running_constraints['after']
        before = running_constraints['before']
        # after = 3
        # before = 2
=======
                     running_constraints: TwitterRunningConstraints) -> List[
        Dict]:

        after = running_constraints['after']
        before = running_constraints['before']
>>>>>>> fixed .gitignore to remove Output/ and add Example/
        size = running_constraints['size']
        fields = running_constraints['fields']
        sort = running_constraints['sort']

<<<<<<< HEAD
        only_download_full_day(self.frequency, before, after)

        date_since = str(self.time_since) 
        date_until = str(self.time_until)

        # NOTE: My fix
        # query = ' AND '.join(self.collection) if len(
        #     self.collection) > 0 else self.collection
        query = ' OR '.join(self.collection) if len(
            self.collection) > 0 else self.collection

        if size is None:
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query) \
                .setSince(date_since) \
                .setUntil(date_until) \
=======
        if self.frequency == 'day':
            date_since = str((datetime.datetime.now() - datetime.timedelta(days=after)).date())
            date_until = str((datetime.datetime.now() - datetime.timedelta(days=before)).date())
        else:
            raise NotImplementedError
        query = ' Or '.join(self.collection)
        if size is None:
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query) \
                .setSince(date_since) \
                .setUntil(date_until)\
>>>>>>> fixed .gitignore to remove Output/ and add Example/
                .setLang('en')

        else:
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query) \
                .setSince(date_since) \
                .setUntil(date_until) \
                .setMaxTweets(size) \
                .setLang('en')

        s = time.time()
<<<<<<< HEAD
        # res = got.manager.TweetManager.getTweets(tweetCriteria,debug=True)
        res = got.manager.TweetManager.getTweets(tweetCriteria)
        # print(res)
=======
        res = got.manager.TweetManager.getTweets(tweetCriteria)
>>>>>>> fixed .gitignore to remove Output/ and add Example/
        f = time.time()
        self.total_request_time_in_milli_second = (f - s) * 1000

        return res

    def run(self,
            before: Optional[int],
            after: int
<<<<<<< HEAD
            ) -> Optional[Tuple[Dict[str, Dict], int]]:

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
=======
            ) -> Dict[str, Dict]:

        try:
            responds_content = self.run_once(before, after)

            total_result = responds_content['metadata']['total_results']
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
>>>>>>> fixed .gitignore to remove Output/ and add Example/
                raise NotImplementedError(
                    f"exception occur in {self.run.__name__}")
            else:
                raise Warning(str(e))

<<<<<<< HEAD
        return responds_content, total_result
=======
        return responds_content
>>>>>>> fixed .gitignore to remove Output/ and add Example/

    @my_timer
    def run_once(self,
                 before: int,
                 after: int
<<<<<<< HEAD
                 ) -> Optional[Dict]:
=======
                 ) -> Dict:
>>>>>>> fixed .gitignore to remove Output/ and add Example/

        running_constraints = self.prepare_running_crawler(before, after)

        res = self.get_responds(running_constraints)
<<<<<<< HEAD
        if res is None:
            return
        else:
            reponds_content = self.apply_crawling_strategy(running_constraints,
                                                           res)
=======
        reponds_content = self.apply_crawling_strategy(running_constraints,
                                                       res)
>>>>>>> fixed .gitignore to remove Output/ and add Example/
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
<<<<<<< HEAD
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
=======
            self.timestamp_utc = datetime.datetime.now() - datetime.timedelta(
                days=after)
        else:
            raise NotImplementedError

        self.current_condition_str = f'collection_name = {self.collection_name} || search_type = {self.search_type} ||' \
                                     f' respond_type = {self.respond_type}|| {after} <= x < {before} '
>>>>>>> fixed .gitignore to remove Output/ and add Example/

        return running_constraints

    def after_run(self):
        raise NotImplementedError


<<<<<<< HEAD
# note: In constrast to TwitterCrawlerCondition, RedditCrawlerCondition need aspect because aspect is used to group 'subreddit' into collection to reflect aspect sentiment
=======
>>>>>>> fixed .gitignore to remove Output/ and add Example/
class TwitterCrawlerCondition(TypedDict):
    crawler_class: Type[TwitterCrawler]
    collection_class: TwitterCollection
    interval: int
    request_timestamp: datetime.datetime
    respond_type: str
    search_type: str
    frequency: str
<<<<<<< HEAD
    aspect: Optional[str]
    max_after: int


def run_twitter_crawler(
        twitter_crawler_condition: TwitterCrawlerCondition) -> List[int]:

=======


def run_twitter_crawler(
        twitter_crawler_condition: TwitterCrawlerCondition) -> None:
>>>>>>> fixed .gitignore to remove Output/ and add Example/
    # TODO
    #   > add fields to _check_that_all_selceted_fields_are_returns # disable option fields = None imply all; its useless
    #   > test and check that all types are assigned appropriately
    #   > finished implement just so that program can be runed (for Twitter), so I can test it by running the program

<<<<<<< HEAD
    def print_twitter_cralwer_condition():
        print('twitter_crawler_condition = ')
        for i, j in twitter_crawler_condition.items():
            print(f'    {i}: {j}')

    print_twitter_cralwer_condition()

    total_returned_data = 0

=======
>>>>>>> fixed .gitignore to remove Output/ and add Example/
    crawler_class: Type[TwitterCrawler] = twitter_crawler_condition[
        'crawler_class']
    twitter_collection_class = twitter_crawler_condition['collection_class']
    interval = twitter_crawler_condition['interval']
    request_timestamp = twitter_crawler_condition['request_timestamp']
    respond_type = twitter_crawler_condition['respond_type']
    search_type = twitter_crawler_condition['search_type']
    frequency = twitter_crawler_condition['frequency']
<<<<<<< HEAD
    max_after = twitter_crawler_condition['max_after']
    # aspect = twitter_crawler_condition['collection_class']['collection']['aspect']

=======

    max_after = 100
>>>>>>> fixed .gitignore to remove Output/ and add Example/
    if frequency == 'day':
        interval_collection: List[int] = [days_to_subtract for days_to_subtract
                                          in list(range(max_after))[::interval]]
    else:
        raise NotImplementedError('')

    interval_range = list(
<<<<<<< HEAD
        zip(interval_collection[:-1], interval_collection[1:]))[::-1]
    # interval_range = list(
    #     zip(interval_collection[:-1], interval_collection[1:]))

    for ind, (before, after) in enumerate(interval_range[:3]):
=======
        zip(interval_collection[:-1], interval_collection[1:]))

    for before, after in interval_range:
>>>>>>> fixed .gitignore to remove Output/ and add Example/
        twitter_crawler = crawler_class(
            twitter_collection_class=twitter_collection_class,
            respond_type=respond_type,
            search_type=search_type,
            frequency=frequency,
<<<<<<< HEAD
            # aspect=aspect,
            verbose=True)
=======
            verbose=False)
>>>>>>> fixed .gitignore to remove Output/ and add Example/

        print(f" || day interval = {interval}")

        try:
<<<<<<< HEAD

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
=======
            responds_content = twitter_crawler.run(before, after)

            saved_file = get_saved_file_path(twitter_crawler.timestamp_utc,
                                             path_name=BASE_DIR /  f'Outputs/Data/{twitter_crawler.crawler_name}/{twitter_crawler.collection_name}/{twitter_crawler.search_type}/{twitter_crawler.respond_type}')
            save_to_file(responds_content,
                         saved_file)
            print('')
>>>>>>> fixed .gitignore to remove Output/ and add Example/
        except Exception as e:
            if str(e) != 'responds are empty':
                print(e)
                raise NotImplementedError(
                    f"unknown error occur in {run_twitter_crawler.__name__} ")
<<<<<<< HEAD
    print(
        f'|| total returned data = {total_returned_data}')
    print(' >>>> finished crawling data <<<<')
    print()
    return total_returned_data
=======

    print(' >>>> finished crawling data <<<<')
>>>>>>> fixed .gitignore to remove Output/ and add Example/


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
<<<<<<< HEAD
    def convert_tweets_to_dict(x): return vars(x)

    def ensure_json(res: Dict) -> Json:
=======
    convert_tweets_to_dict = lambda x: vars(x)

    def ensure_json(res: Dict)-> Json:
>>>>>>> fixed .gitignore to remove Output/ and add Example/
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
        # HERE I need to convert
        pass

    def check_responses_consistency(res: Json) -> None:

        if len(res['data']) > 0:
            for i in range(len(res['data'])):
                pass

                # HERE >
                #   : check aggs key and metadata keys
                #   : did I have
                #   : check type of keys name
                #  :check that aggs val is valid (consider changing name to created_utc look at point above)
                #  :add fields to _check_that_all_selceted_fields_are_returns # disable option fields = None imply all; its useless
                #   _check_that_all_selected_fields_are_returns(
                #     running_constraints,
                #     res,
                #     i,
                #     crawler_instance.current_condition_str,
                #     crawler_instance.verbose)
        else:
            raise Warning('responds are empty')
<<<<<<< HEAD
    
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



=======

    check_responses_consistency(res_data_dict)

>>>>>>> fixed .gitignore to remove Output/ and add Example/
    return res_data_dict


def _get_twitter_aggs(res: Json,
                      running_constraints: TwitterRunningConstraints,
                      crawler_instance: TwitterCrawler,
                      ) -> Json:
    aggs_dict: TwitterAggs

    if 'aggs' not in res:
        def aggs_doc_count_per_frequency() -> doc_count_per_frequency:
            x: Dict[str, int]
            x = {}
            counter = {}
            doc_count_dict = {}
<<<<<<< HEAD
            get_date_datetime_from_epoch_datetime = lambda \
                x: datetime.datetime.fromtimestamp(x).date()

            def convert_datetime_to_epoch_datetime(x): return \
                str(datetime.datetime(x.year, x.month,
                                      x.day).timestamp()).split(
                    '.')[0]
=======
            get_date_datetime_from_epoch_datetime = lambda x: datetime.datetime.fromtimestamp(x).date()
            convert_datetime_to_epoch_datetime = lambda x: str(datetime.datetime(x.year, x.month, x.day).timestamp()).split('.')[0]
>>>>>>> fixed .gitignore to remove Output/ and add Example/
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
<<<<<<< HEAD
                          aspect: Tags,
                          query: Query,
                          ) -> Json:

    after = running_constraints['after']
    before = running_constraints['before']
=======
                          ) -> Json:
    after = running_constraints['after']
>>>>>>> fixed .gitignore to remove Output/ and add Example/
    size = running_constraints['size']
    sort = running_constraints['sort']
    fields = running_constraints['fields']

<<<<<<< HEAD
    keys = ['running_constraints', 'after', 'aggs', 'before',
            'execution_time_milliseconds', 'frequency', 'index',
            'results_returned', 'size', 'sort', 'timed_out',
            'search_words', 'total_results', 'fields', 'aspect',  'query']

    def create_metadata() -> TwitterMetadata:
        x = {'running_constraints': running_constraints,
             'after': after,
             'before': before,
=======
    def create_metadata() -> TwitterMetadata:
        x = {'running_constraints': running_constraints,
             'after': after,
>>>>>>> fixed .gitignore to remove Output/ and add Example/
             'aggs': list(res['aggs'].keys()),
             'execution_time_milliseconds': crawler_instance.total_request_time_in_milli_second,
             'frequency': crawler_instance.frequency,
             'size': size,
             'sort': sort,
             'search_words': crawler_instance.collection,
             'total_results': len(res['data']),
<<<<<<< HEAD
             'fields': fields,
             'aspect': aspect,
             'query': query,
             'results_returned': None,
             'timed_out': None,
             'index': None,
             }

        assert len(set(list(x.keys())) ^ set(keys)) == 0
=======
             'fields': fields}
>>>>>>> fixed .gitignore to remove Output/ and add Example/

        return x

    if 'metadata' not in res:
        aggs_dict: TwitterAggs
        res['metadata'] = create_metadata()

        return res
    else:
<<<<<<< HEAD
        # NOTE: why do I need else section here? can't I just add metadata to the data? 
=======
        keys = ['running_constraints', 'after', 'aggs', 'before',
                'execution_time_milliseconds', 'frequency', 'index',
                'results_returned', 'size', 'sort', 'timed_out',
                'search_words', 'total_results', 'fields']

>>>>>>> fixed .gitignore to remove Output/ and add Example/
        assert len(res['metadata']) == len(keys), ''

        for i in keys:
            if i not in res['metadata']:
                raise ValueError('')
