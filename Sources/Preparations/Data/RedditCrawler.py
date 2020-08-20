import datetime
import json
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Type

import numpy as np  # type: ignore
import requests
from typing_extensions import TypedDict

from Sources.Preparations.Features.sentiment_analysis import get_sentiment
from Test_dir.test_conditions import \
    _check_that_all_selected_fields_are_returns
from Test_dir.test_conditions import check_response_keys
from Utilities import get_full_datetime_str
from Utilities import get_saved_file_path
from Utilities import my_timer
from Utilities import save_to_file
from Utilities.control_limit import ControlLimit
from Utilities.declared_typing import Frequency
from Utilities.declared_typing import Json
from Utilities.declared_typing import RedditResponse
from Utilities.declared_typing import RedditRunningConstraints
from Utilities.declared_typing import SubredditCollection
from Utilities.declared_typing import Url
from Utilities.declared_typing import Tags
from Utilities.declared_typing import Query
from Utilities.time_utility import _convert_timedelta_to_specified_frequency
from Utilities.time_utility import _get_epoch_datetime_subtract_timedelta
from Utilities.ensure_type import only_download_full_day

from global_parameters import ALL_REDDIT_TAGS
from global_parameters import BASE_DIR
from global_parameters import KNOWN_ERROR


class RedditCrawler:
    def __init__(self,
                 subreddits_collection_class: SubredditCollection,
                 respond_type: str,
                 search_type: str,
                 frequency: Frequency,
                 verbose: int,
                 aspect: str,
                 max_after: int):

        self.crawler_name = 'RedditCrawler'
        self.verbose = verbose
        self.prepare_crawler(subreddits_collection_class,
                             respond_type,
                             search_type,
                             frequency,
                             aspect,
                             max_after)

    def prepare_crawler(self,
                        subreddits_collection_class: SubredditCollection,
                        respond_type: str,
                        search_type: str,
                        frequency: Frequency,
                        aspect: str,
                        max_after: int) -> None:

        self.respond_type = respond_type
        self.search_type = search_type
        self.frequency = frequency
        self.collection_name = subreddits_collection_class['name']
        self.collection = subreddits_collection_class['collection']
        self.aspect = aspect
        self.query = self.collection['query']
        self.max_after = max_after

    def prepare_running_crawler(self,
                                before: Optional[int],
                                after: int,
                                max_after: int) -> RedditRunningConstraints:

        common_fields = 'author, author_flair_richtext, author_flair_type, ' \
                        'author_fullname,id, created_utc, permalink, retrieved_on, score, ' \
                        'subreddit, subreddit_id, total_awards_received, stickied, all_awardings'

        subreddit_fields = " domain, full_link, is_original_content, is_self, num_comments, pinned, selftext, subreddit_subscribers, title, upvote_ratio"

        comment_fields = 'body,parent_id,link_id'

        now = datetime.datetime.now()
        self.timestamp_utc = _get_epoch_datetime_subtract_timedelta(
            now, self.frequency, after)

        max_after_timestamp_utc = _get_epoch_datetime_subtract_timedelta(
            now, 'day', max_after)

        # FIXME: fix this error
        assert self.timestamp_utc >= max_after_timestamp_utc, f'{self.timestamp_utc}, {max_after_timestamp_utc}, {after}'

        def replace_and_split(x): return x.replace(' ', '').split(',')
        fields = replace_and_split(common_fields) + replace_and_split(
            subreddit_fields) + replace_and_split(comment_fields)
        fields = ','.join(fields)

        running_constraints: RedditRunningConstraints
        running_constraints = {
            'before': before,
            'after': after,
            'aggs': 'created_utc',
            'size': 1000,
            'metadata': 'true',
            'sort': 'asc',
            'fields': fields,
        }

        if self.frequency == 'day':
            self.time_since = datetime.datetime.now().date() - datetime.timedelta(
                days=after)

            if before is not None:
                self.time_until = datetime.datetime.now().date() - datetime.timedelta(
                    days=before) 

            else:
                self.time_until = datetime.datetime.now().date()
        else:
            raise NotImplementedError

        self.current_condition_str = f' aspect = {self.aspect} -> query = {self.query}||collection_name = {self.collection_name} || search_type = {self.search_type} ||' \
                                     f' respond_type = {self.respond_type}|| frequency = {self.frequency} || {after} <= x < {before} || {str(self.time_since)} to {str(self.time_until)}'

        if self.verbose:
            print(
                f" {self.current_condition_str}")


        return running_constraints

    def get_url(self, running_constraints: RedditRunningConstraints) -> Url:
        # frequency = running_constraints['frequency']
        before = running_constraints['before']

        def _get_after_frequency():
            if self.frequency == 'day':
                after_frequency = 'd'
            elif self.frequency == 'hour':
                after_frequency = 'h'
            elif self.frequency == 'minute':
                after_frequency = 'm'
            elif self.frequency == 'second':
                after_frequency = 's'
            else:
                raise NotImplementedError
            return after_frequency

        after_frequency = _get_after_frequency()

        if self.aspect is None:
            endpoint_url = self._get_url_endpoint_without_query_param(
                running_constraints, after_frequency)
        elif self.aspect in ALL_REDDIT_TAGS:
            endpoint_url = self._get_url_endpoint_with_query_param(
                running_constraints, after_frequency)
        else:
            raise NotImplementedError

        if before is not None:
            endpoint_url += f'&before={before}{after_frequency}'

        return endpoint_url

    @my_timer
    # @signature_logger
    def get_responds(self,
                     running_constraints: RedditRunningConstraints) -> Json:

        before = running_constraints['before']
        after = running_constraints['after']

        only_download_full_day(self.frequency, before, after)

        endpoint_url = self.get_url(running_constraints)

        # HERE try to catch json error
        def ensure_json(res):
            # BUG In RedditCrawler, json.loads(res.text) sometimes caused error at the first iteration (not sure why)
            # NOTE: I dont use try-except here because this may reminds you of subtle-error
            if res.text is not None:
                res_text = res.text
                return json.loads(res_text)  # type = json
            else:
                return None

        res = ensure_json(requests.get(endpoint_url))
        check_response_keys(res)

        return res

    @my_timer
    # @signature_logger
    def get_submission_avg_per_day(self,
                                   res: Json) -> float:

        def check_required_key():
            assert 'aggs' in res and 'data' in res, ''

        check_required_key()

        created_utc = res['aggs']['created_utc']
        num_interval = len(created_utc)

        total = 0
        for ind, key in enumerate(created_utc):
            total += key['doc_count']

        avg = total / num_interval

        if self.verbose:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(
                f' {self.current_condition_str} ||  avg_per_{self.frequency} given {num_interval} {self.frequency}s || {avg}')  # pass in variable to be pretty printedJ

        return avg

    def run(self,
            before: Optional[int],
            after: int,
            max_after: int) -> Tuple[Dict[str, Dict], int, int]:

        control_limit = ControlLimit()
        try:
            responds_content = self.run_once(before, after, max_after)
            total_result = responds_content['metadata']['total_results']
            missing_results = 1000 - total_result
            missing_results = 0 if np.sign(
                missing_results) > 0 else missing_results
            if self.verbose:
                print(
                    f" {self.current_condition_str} || total_results = {total_result} || missing_result = {missing_results}")
            else:
                print(f'missing_reulst = {missing_results}')
            returned_results = total_result - missing_results
        except Exception as e:
            if str(e) not in KNOWN_ERROR:
                raise NotImplementedError(
                    f"exception occur in {self.run.__name__}")
            else:
                raise Warning(str(e))

        control_limit.control_pushshift_limit(total_number_of_request=1)

        return responds_content, returned_results, missing_results

    @my_timer
    # @signature_logger
    def run_once(self,
                 before: Optional[int],
                 after: int,
                 max_after: int) -> Dict:
        try:
            running_constraints = self.prepare_running_crawler(before,
                                                               after,
                                                               max_after)
            res = self.get_responds(running_constraints)
            reponds_content = self.apply_crawling_strategy(running_constraints,
                                                           res)
            return reponds_content
        except Exception as e:
            if str(e) not in KNOWN_ERROR:
                raise NotImplementedError(
                    f"unknown error occur in {self.run_once.__name__} ")
            else:
                raise ValueError(str(e))

    def adjust_after_step(self,
                          per_interval_average: float,
                          max_responds_size: int) -> int:
        max_responds_threshold = max_responds_size - int(
            max_responds_size * 0.40)
        time_interval = int(max_responds_threshold / per_interval_average)
        time_interval = 1 if time_interval < 1 else time_interval
        return time_interval

    def get_submission_data(self,
                            running_constraints: RedditRunningConstraints,
                            res: Json) -> RedditResponse:
        try:
            res = _get_reddit_data(res, running_constraints, self)
            # _get_reddit_aggs(res)
            res = _get_reddit_metadata(res, running_constraints,self.aspect ,self.query)

            check_response_keys(res)
        except Exception as e:
            if str(e) != 'responds are empty':
                raise NotImplementedError(
                    f"unknown error occur in {self.get_submission_data.__name__} ")
            else:
                raise ValueError(str(e))

        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(
        #     f' {self.current_condition_str} respond data => {self.per_day_average}')  # pass in variable to be pretty printedj

        return res

    def apply_crawling_strategy(self,
                                running_constraints: RedditRunningConstraints,
                                res: Json) -> RedditResponse:
        try:
            if self.respond_type == 'avg':
                raise DeprecationWarning(
                    f'no longer support {self.respond_type}')

            elif self.respond_type == 'data':
                return self.get_submission_data(running_constraints,
                                                res)
            else:
                raise ValueError('')
        except Exception as e:
            if str(e) != 'responds are empty':
                raise NotImplementedError(
                    f"unknown error occur in {self.apply_crawling_strategy.__name__} ")
            else:
                raise ValueError(str(e))

    def after_run(self,
                  res: Json,
                  after: int,
                  max_after: int
                  ) -> Tuple:
        per_interval_average: float = self.get_submission_avg_per_day(
            res)

        next_interval: int = self.adjust_after_step(per_interval_average,
                                                    max_responds_size=1000)

        # next_before, next_after, next_interval = self._update_interval_before_after(after, max_after, next_interval)
        next_interval = max_after if next_interval > max_after else next_interval

        return next_interval, per_interval_average
        # return next_interval, per_interval_average, next_before, next_after

    def _get_url_endpoint_with_query_param(self,
                                           running_constraints: RedditRunningConstraints,
                                           after_frequency: str
                                           ):
        aggs = running_constraints['aggs']
        after = running_constraints['after']
        size = running_constraints['size']
        metadata = running_constraints['metadata']
        sort = running_constraints['sort']
        fields = running_constraints['fields']

        all_subreddits: str = ','.join(self.collection['subreddit'])
        all_queries: str = '|'.join(self.collection['query'])

        endpoint_url = f'https://api.pushshift.io/reddit/search/{self.search_type}/?' \
                       f'&subreddit={all_subreddits}' \
                       f'&q={all_queries}' \
                       f'&after={after}{after_frequency}' \
                       f'&size={size}' \
                       f'&metadata={metadata}' \
                       f'&sort={sort}' \
                       f'&fields={fields}' \
                       f'&aggs={aggs}' \
                       f'&frequency={self.frequency}'
        return endpoint_url

    def _get_url_endpoint_without_query_param(self,
                                              running_constraints: RedditRunningConstraints,
                                              after_frequency: str) -> Url:
        aggs = running_constraints['aggs']
        after = running_constraints['after']
        size = running_constraints['size']
        metadata = running_constraints['metadata']
        sort = running_constraints['sort']
        fields = running_constraints['fields']

        all_subreddit: str = ','.join(self.collection['subreddit'])
        endpoint_url = f'https://api.pushshift.io/reddit/search/{self.search_type}/?' \
                       f'&subreddit={all_subreddit}' \
                       f'&after={after}{after_frequency}' \
                       f'&size={size}' \
                       f'&metadata={metadata}' \
                       f'&sort={sort}' \
                       f'&fields={fields}' \
                       f'&aggs={aggs}' \
                       f'&frequency={self.frequency}'
        return endpoint_url

    def _update_interval_before_after(self,
                                      after: int,
                                      max_after_with_specified_frequency: int,
                                      next_interval: int) -> Tuple:
        # HERE
        #  >this only works for day ( don't use max_after, use max_after of the same frequency

        next_before: int = max_after_with_specified_frequency if after + \
            1 >= max_after_with_specified_frequency else after + 1
        next_after: int = max_after_with_specified_frequency if next_before + \
            next_interval >= max_after_with_specified_frequency else next_before + next_interval  # type: ignore

        # next_interval: int = next_before - next_after
        next_interval: int = next_after - next_before

        return next_before, next_after, next_interval


class RedditCrawlerCondition(TypedDict):
    crawler_class: Type[RedditCrawler]
    collection_class: SubredditCollection
    initial_interval: int
    request_timestamp: datetime.datetime
    respond_type: str
    search_type: str
    frequency: str
    verbose: bool
    aspect: Optional[str]
    max_after: int


def run_reddit_crawler(
        reddit_crawler_condition: RedditCrawlerCondition,
):
    crawler_class: Type[RedditCrawler] = reddit_crawler_condition[
        'crawler_class']
    subreddits_collection_class = reddit_crawler_condition['collection_class']
    initial_interval = reddit_crawler_condition['initial_interval']
    request_timestamp = reddit_crawler_condition['request_timestamp']
    respond_type = reddit_crawler_condition['respond_type']
    search_type = reddit_crawler_condition['search_type']
    frequency = reddit_crawler_condition['frequency']
    verbose = reddit_crawler_condition['verbose']
    max_after = reddit_crawler_condition['max_after']
    aspect = reddit_crawler_condition['collection_class']['collection']['aspect']

    after = initial_interval
    before = None
    next_interval = None
    frequency = frequency  # , 'second', 'minute', 'day'
    assert after <= max_after, 'after have to be less than max_after'
    saved_path = None

    max_after_epoch_datetime = _get_epoch_datetime_subtract_timedelta(
        datetime.datetime.now(), 'day', max_after)
    max_after_epoch_datetime_date = max_after_epoch_datetime.date()

    def _select_optimize_frequency(before: Optional[int] = None,
                                   after: int = 100):
        print(
            'selecting optimized frequency length among: day, hour, minute, second ')
        sorted_frequency_rank = ['day', 'hour', 'minute', 'second']

        def _count_num_missing_value(res: Json) -> int:
            num_missing_val = res['metadata']['total_results'] - len(
                res['data'])
            return num_missing_val

        condition = True

        while condition:
            frequency = sorted_frequency_rank[0]

            reddit_crawler = crawler_class(
                subreddits_collection_class=subreddits_collection_class,
                respond_type=respond_type,
                search_type=search_type,
                frequency=frequency,
                verbose=verbose,
                aspect=aspect,
                max_after=max_after
            )

            responds_content, _, _ = reddit_crawler.run(before, after,
                                                        max_after)

            if len(responds_content['data']) > 0:
                if _count_num_missing_value(
                        responds_content) > 0:  # if next_interval (predicted_interval) still have too many respon
                    next_interval, per_day_average = reddit_crawler.after_run(
                        responds_content, after, max_after)

                    if next_interval == 1 and per_day_average > 1000:  # if there are too many responds per day
                        sorted_frequency_rank = sorted_frequency_rank[1:]

                        print(
                            f' || adjust frequency from {reddit_crawler_condition["frequency"]} to {sorted_frequency_rank[0]}')
                        print()

                        reddit_crawler_condition[
                            'frequency'] = sorted_frequency_rank[0]
                    else:
                        # after = max_after if next_interval > max_after else next_interval
                        after = next_interval  # assigned predicted interval

                        assert after <= max_after, ''
                    
                        print(
                            f' Given frequency = {frequency} || adjust initial_interval(after) from {reddit_crawler_condition["initial_interval"]} to {after}')
                        print()

                        reddit_crawler_condition['initial_interval'] = after

                    return after, frequency
                else:
                    after_timestamp_utc = _get_epoch_datetime_subtract_timedelta(
                        datetime.datetime.now(), frequency, after)

                    time_diff = datetime.datetime.now() - after_timestamp_utc

                    after = _convert_timedelta_to_specified_frequency(
                        time_diff, frequency)

                    reddit_crawler_condition['initial_interval'] = after
                    reddit_crawler_condition[
                        'frequency'] = frequency
                    print(
                        f"Given frequency = {frequency} || after is set to {reddit_crawler_condition['initial_interval']}")
                    print()

                    return after, frequency
            else:
                if after >= max_after:
                    raise ValueError(
                        'responses are empty')  # HERE figure out how to deal with respond_content is empty
                else:
                    raise NotImplementedError

    # VALIDATE I validated it, but it may missed something, so this is left here for future debugging
    after, frequency = _select_optimize_frequency(after=max_after)
    assert after <= max_after, ''

    total_returned_data = 0
    total_missing_data = 0

    request_timestamp_str = get_full_datetime_str(request_timestamp)

    max_after_delta = _get_epoch_datetime_subtract_timedelta(
        datetime.datetime.now(), 'day', max_after)
    # max_after_delta = _get_epoch_datetime_subtract_timedelta(datetime.datetime.now(), frequency, max_after )
    time_diff = datetime.datetime.now() - max_after_delta

    max_after_with_specified_frequency = _convert_timedelta_to_specified_frequency(
        time_diff, frequency)

    # optimize can I optimize while with do-while?
    # while after <= max_after:
    terminal_condition = True
    while terminal_condition:

        reddit_crawler = crawler_class(
            subreddits_collection_class=subreddits_collection_class,
            respond_type=respond_type,
            search_type=search_type,
            frequency=frequency,
            verbose=verbose,
            aspect=aspect,
            max_after=max_after)

        interval = next_interval if next_interval is not None else after

        # print(
        #     f' interval = {interval} >>> aspect = {aspect} ||collection_name = {subreddits_collection_class["collection"]} || search_type = {search_type} ||'
        #     f' respond_type = {respond_type}|| frequency = {frequency} || {after} <= x < {before} ')

        if aspect is None:
            with_aspects_folder = 'without_aspects'
            saved_path = BASE_DIR / \
                f'Outputs/Data/{reddit_crawler.crawler_name}/{with_aspects_folder}/{reddit_crawler.aspect}/{reddit_crawler.collection_name}/{reddit_crawler.search_type}/{reddit_crawler.respond_type}/{request_timestamp_str}/'
        elif isinstance(aspect, str):
            with_aspects_folder = 'with_aspects'
            saved_path = BASE_DIR / \
                f'Outputs/Data/{reddit_crawler.crawler_name}/{with_aspects_folder}/{reddit_crawler.aspect}/{reddit_crawler.collection_name}/{reddit_crawler.search_type}/{reddit_crawler.respond_type}/{request_timestamp_str}/'
        else:
            raise ValueError('')

        try:
            responds_content, num_returned_data, num_missing_data = reddit_crawler.run(
                before, after, max_after)

            total_returned_data += num_returned_data
            total_missing_data += num_missing_data

            next_interval, per_day_average = reddit_crawler.after_run(
                responds_content, after, max_after)

            saved_file = get_saved_file_path(reddit_crawler.time_since, reddit_crawler.time_until,
                                                path_name=BASE_DIR / f'Outputs/Data/{reddit_crawler.crawler_name}/{reddit_crawler.aspect}/{reddit_crawler.collection_name}/{reddit_crawler.search_type}/{reddit_crawler.respond_type}')
            save_to_file(responds_content,
                            saved_file)
        except Exception as e:

            if str(e) not in KNOWN_ERROR:
                raise NotImplementedError(
                    f"unknown error occur in {run_reddit_crawler.__name__} ")
            else:
                print('responds are empty')
                next_interval = after  # reintialize next-interval to be last calculated per_day_average

        # if reddit_crawler.timestamp_utc.date() < max_after_epoch_datetime_date:
        #     reddit_crawler.timestamp_utc = max_after_epoch_datetime

        # after = _ensure_datetime_for_specified_frequency_not_consider_max_after(
        #     reddit_crawler.timestamp_utc, max_after_epoch_datetime,
        #     frequency, after)
        if after == max_after_with_specified_frequency:
            terminal_condition = False

        reddit_crawler.timestamp_utc = _get_epoch_datetime_subtract_timedelta(
            reddit_crawler.timestamp_utc, reddit_crawler.frequency,
            next_interval)

        before, after, next_interval = reddit_crawler._update_interval_before_after(
            after, max_after_with_specified_frequency, next_interval)

        # HERE check if the line of code below causes error
        assert after <= max_after_with_specified_frequency, ''

    print(
        f'|| total returned data = {total_returned_data} || total_missing_data = {total_missing_data}')
    print(' >>>> finished crawling data <<<<')
    print()
    return total_returned_data, total_missing_data


# =====================
# ==Reddit Test
# =====================
def _get_reddit_metadata(res: Json,
                         running_constraints: RedditRunningConstraints,
                         aspect: str,
                         query: Query) -> Json:
    metadata = {}
    metadata['running_constraints'] = running_constraints

    keys = ['total_results', 'before', 'after', 'frequency',
            'execution_time_milliseconds', 'sort', 'fields',
            'subreddit']

    # filter out fields that we don't want
    for key in keys:
        metadata[key] = res['metadata'][key]

    res['metadata'] = metadata

    # add fields that are not provided by pushshift api
    res['metadata']['aspect'] = aspect
    res['metadata']['query'] = query

    return res


@my_timer
def _get_reddit_data(res: Json,
                     running_constraints: RedditRunningConstraints,
                     crawler_class: RedditCrawler) -> Json:

    def _check_responds_consistency():
        if len(res['data']) > 0:
            for i in range(len(res['data'])):
                _check_that_all_selected_fields_are_returns(
                    running_constraints,
                    res,
                    i,
                    crawler_class.current_condition_str,
                    crawler_class.verbose)
        else:
            # print('response are empty')
            raise Warning('responds are empty')

    # @my_timer
    def _get_sentiment(x) -> float:

        text: Optional[str]

        if crawler_class.search_type == 'comment':
            text = x['body']
        elif crawler_class.search_type == 'submission':
            text = x['title']
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
        if str(e) != 'responds are empty':
            raise NotImplementedError(
                f"unknown error occur in {_get_reddit_data.__name__} ")
        else:
            raise ValueError(str(e))

    from tqdm import tqdm
    all_data_with_sentiment = []
    for data in tqdm(res['data']):
        data_with_sentiment = data
        data_with_sentiment['sentiment'] = _get_sentiment(data)
        all_data_with_sentiment.append(data_with_sentiment)
        # data['sentiment'] = _get_sentiment(data)

    res['data'] = all_data_with_sentiment

    return res


def _get_reddit_aggs(res: Json) -> None:
    raise NotImplementedError
