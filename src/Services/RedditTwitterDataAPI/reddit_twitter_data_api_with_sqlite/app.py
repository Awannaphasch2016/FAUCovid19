#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Run social media data api so users can requests for social media data"""

import datetime
import os
import sqlite3
from flask import Flask
from flask import request
from flask_restful import Api
from itertools import product
from os import walk
from typing import Dict
from typing import List

# Create an instance of Flask
# from global_parameters import BASE_DIR

app = Flask(__name__)

# Create the API
api = Api(app)

# /?crawlers=twitter&since=2020-08-07&until=2020-08-08&aspects=work_from_home,reopen
DATEFORMAT = "%Y-%m-%d"

ALL_ASPECTS = ['work_from_home', 'social_distance',
               'corona', 'reopen', 'lockdown']
ALL_CRALWERS = ['twitter', 'reddit']
ALL_FREQUENCY = ['day']
ALL_REDDIT_SEARCH_TYPE = ['comment', 'submission']
ALL_TWITTER_SEARCH_TYPE = ['data_tweet']

ALL_REDDIT_FEILDS = ['aspect', 'created_utc', 'search_types', 'crawler',
                     'frequency',
                     'subreddit', 'link_id', 'parent_id', 'title', 'body', 'id'
                     ]
ALL_TWITTER_FEILDS = ['crawler', 'text', 'date', 'search_type', 'aspect',
                      'frequency', 'sentiment', 'id']


def is_reddit_fields(s):
    """
    return true if arg is an accepted reddit's fields

    :type s: str
    :param s: any accepted fields

    :rtype: boolean
    :return: return true if arg is an accpeted reddit fields otherwise false
    """
    return s in ALL_REDDIT_FEILDS or s == 'all'


def is_twitter_fields(s):
    """
    return true if arg is an accepted twitter's fields

    :type s: str
    :param s: any accepted fields

    :rtype: boolean
    :return: return true if arg is an accpeted twitter fields otherwise false
    """
    return s in ALL_TWITTER_FEILDS or s == 'all'


import pathlib


class APIManager:
    def __init__(self, aspects, crawlers, after_date, before_date, frequency,
                 search_types, fields):

        self.init_vars(aspects, crawlers, after_date, before_date, frequency,
                       search_types, fields)

    def init_vars(self, aspects, crawlers, after_date, before_date, frequency,
                  search_types, fields):
        """
        prepare common data that will be used among class's methods

        :type aspects: List of str
        :param aspects: list of aspects

        :type crawlers: List of str
        :param crawlers: list of aspects

        :type after_date: datetime.datetime
        :param after_date: date in which all aata AFTER this date should be retrieved

        :type before_date: datetime.datetime
        :param before_date: date in which all aata BEFORE this date should be retrieved

        :type frequency: Frequency
        :param frequency: interval of time to retrieved data

        :type search_types: list of str
        :param search_types: list of desired search type by crawler

        :type fields: list of str
        :param fields: list of desired fields by crawler

        """

        self.aspects = aspects
        self.crawlers = crawlers
        self.after_date = after_date
        self.before_date = before_date
        self.frequency = frequency
        self.search_types = search_types
        self.fields = fields

    def get_all_retrived_data(self):
        """
        prepared + return all  stored crawled data of a specified crawler to browser
        """

        returned_data = {}

        def _get_query(crawler, all_crawler_search_type, all_crawler_fields):
            after_date_query = ""
            before_date_query = ""

            if self.after_date[0] is None and self.before_date[0] is None:
                after_date_query = ''
                before_date_query = ''
            else:
                if crawler == 'reddit':
                    date_key = ' created_utc'
                elif crawler == 'twitter':
                    date_key = ' date '
                else:
                    raise ValueError()

                if self.after_date[0] is not None:
                    after_date_created_utc = int(
                        self.after_date[0].timestamp())
                    after_date_query = f"{date_key} > {after_date_created_utc}"
                if self.before_date[0] is not None:
                    before_date_created_utc = int(
                        self.before_date[0].timestamp())
                    before_date_query = f"{date_key} <= {before_date_created_utc}"

            if self.search_types[0] == 'all':
                search_types = all_crawler_search_type
            else:
                search_types = self.search_types

            if self.fields[0] == 'all':
                fields = all_crawler_fields
                fields_query = " * "
            else:
                fields_query = ','.join(self.fields)

            date_query = ""
            search_types_query = ""
            aspect_query = f" aspect = '{asp}'"

            all_query = ""
            frequency_query = ""

            if len(search_types) == len(all_crawler_search_type):
                all_query = [aspect_query]
            else:
                tmp = []
                for t in search_types:
                    tmp.append(f" search_type = '{t}' ")
                tmp = ' or '.join(tmp)
                tmp = " ( " + tmp + " ) "
                all_query = [aspect_query, tmp]

            # all_reddit_data = " and ".join([aspect_query, search_types])

            if len(after_date_query) > 0 and len(before_date_query) > 0:
                all_query.append(after_date_query)
                all_query.append(before_date_query)
            elif len(after_date_query) > 0:
                all_query.append(after_date_query)
            elif len(before_date_query) > 0:
                all_query.append(before_date_query)
            elif len(before_date_query) == 0 and len(after_date_query) == 0:
                pass
            else:
                raise ValueError

            if self.frequency[0] is not None:
                frequency_query = f" frequency = '{self.frequency[0]}' "
                all_query.append(frequency_query)

            print()

            return f"select {fields_query} from {crawler} where ".format(
                fields_query, crawler) + " and ".join(all_query)

        for asp, crawler in product(self.aspects, self.crawlers):
            if crawler == 'twitter':
                crawler_folder = 'TwitterCrawler'
            elif crawler == 'reddit':
                crawler_folder = 'RedditCrawler'
            else:
                raise ValueError()

            if crawler == 'reddit':
                # path_to_reddit_database = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Examples\Demo\CrawlDataFromSocialNetwork\RedditTwitterDataAPI\reddit_twitter_data_api_with_sqlite\reddit_database'
                # path_to_reddit_database = pathlib.Path(BASE_DIR) / r'Examples\Demo\CrawlDataFromSocialNetwork\RedditTwitterDataAPI\reddit_twitter_data_api_with_sqlite\reddit_database'
                path_to_reddit_database = r'reddit_database'
                path_to_reddit_database = str(path_to_reddit_database)

                query = _get_query(crawler, ALL_REDDIT_SEARCH_TYPE,
                                   ALL_REDDIT_FEILDS)
                all_reddit_data = self._get_all_data_from_sqlite(crawler,
                                                                 path_to_reddit_database,
                                                                 query)
                returned_data.setdefault('all_retrived_data', []).extend(
                    all_reddit_data)

            if crawler == 'twitter':
                # path_to_twitter_database = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Examples\Demo\CrawlDataFromSocialNetwork\RedditTwitterDataAPI\reddit_twitter_data_api_with_sqlite\twitter_database'
                # path_to_twitter_database = pathlib.Path(BASE_DIR)/ r'Examples\Demo\CrawlDataFromSocialNetwork\RedditTwitterDataAPI\reddit_twitter_data_api_with_sqlite\twitter_database'
                path_to_twitter_database = r'twitter_database'
                path_to_twitter_database = str(path_to_twitter_database)

                query = _get_query(crawler, ALL_TWITTER_SEARCH_TYPE,
                                   ALL_TWITTER_FEILDS)
                all_reddit_data = self._get_all_data_from_sqlite(crawler,
                                                                 path_to_twitter_database,
                                                                 query)
                returned_data.setdefault('all_retrived_data', []).extend(
                    all_reddit_data)

        return returned_data

    def _get_all_data_from_sqlite(self, crawler: str, path_to_database: str,
                                  query: str) -> List[Dict]:
        """
        get all stored crawled data of a specified crawler from sqlite database

        :type  crawler:
        :param crawler:

        :type path_to_database: str
        :param path_to_database: path to dataabase


        :type query: str
        :param query: str of  character to pull data from  database

        :rtype:  list of dict
        :return:  list of dict containing all specified parameters
        """
        assert crawler == path_to_database.split('\\')[-1].split('_')[0]
        # print(path_to_database)
        conn = sqlite3.connect(path_to_database)
        cur = conn.cursor()
        # cur.execute("select * from reddit")
        print(query)
        cur.execute(query)

        def unroll_all_variable_in_fields():
            if self.fields[0] == 'all' and crawler == 'reddit':
                return ALL_REDDIT_FEILDS
            if self.fields[0] == 'all' and crawler == 'twitter':
                return ALL_TWITTER_FEILDS
            return self.fields

        fields = unroll_all_variable_in_fields()

        if 'crawler' in fields:
            r = [{**dict((cur.description[i][0], value) \
                         for i, value in enumerate(row)),
                  **{"crawler": crawler}} for row in cur.fetchall()]
        else:
            r = [{**dict((cur.description[i][0], value) \
                         for i, value in enumerate(row))} for row in
                 cur.fetchall()]
        # self.conn.commit()
        conn.close()
        return r

    def _get_retrieved_data_from_a_file(self, all_data_from_a_file):
        pass

    # def _get_retrieved_data_from_a_file(self, all_data_from_a_file):
    #     retrieved_since_ind = 0
    #     retrieved_until_ind = 0
    #     current_doc_count = 0
    #     since_epoch = datetime.datetime.strptime(self.after_date, DATEFORMAT).timestamp()
    #     until_epoch = datetime.datetime.strptime(self.before_date, DATEFORMAT).timestamp()
    #
    #     all_retrieved_data = 0
    #     for j in all_data_from_a_file['aggs']['created_utc']:
    #         if since_epoch < j['key']:
    #             retrieved_until_ind = current_doc_count
    #         if until_epoch < j['key']:
    #             retrieved_since_ind = current_doc_count
    #         current_doc_count += j['doc_count']
    #
    #     retrieved_data = [i['body'] for i in all_data_from_a_file['data'][retrieved_since_ind:retrieved_until_ind]]
    #
    #     return retrieved_data

    # def get_all_fiile(self, all_data_path, aspect, search_types):
    #     all_files = []
    #     for i in all_data_path:
    #         for (dirpath, dirnames, filenames) in walk(i):
    #             x = dirpath.split('\\')[-1]
    #             y = dirpath.split('\\')[-3]
    #             if x in search_types and y in aspect:
    #                 for (dirpath1, dirnames1, filenames1) in walk(
    #                         pathlib.Path(dirpath)):
    #                     for file in filenames1:
    #                         all_files.append(os.path.join(dirpath1, file))
    #     return all_files


def is_date(date_string):
    '''
    return true if parameter is a date with a specified format (%Y-%m-%d) otherwise false

    :type date_string: str
    :param date_strng: date in the following format %Y-%m-%d

    :rtype: boolean
    :return: return true if arg is an accpeted frequency otherwise flase
    '''
    # format = "%m-%d-%y"
    format = DATEFORMAT

    try:
        x = datetime.datetime.strptime(date_string, format)
        return True
    except ValueError as e:
        print(
            "This is the incorrect date string format. It should be %Y-%m-%d for example 12-25-2018")
        raise ValueError(e)


def is_supported_frequency(freq):
    """
    return true if arg is an accpeted frequency otherwise false

    :type freq: str
    :param freq: any accpeted frequency str

    :rtype: boolean
    :return: return true if arg is an accpeted frequency otherwise false
    """
    return freq in ALL_FREQUENCY or freq is None


# def is_aspect(asp):
#     """
#     return true if arg is an accpeted frequency otherwise false
#
#     :type asp: str
#     :param asp: any accpeted aspects str
#
#     :rtype: boolean
#     :return: return true if arg is an accpeted aspect otherwise false
#     """
#     return asp in ALL_ASPECTS


def is_supported_aspect(asp):
    """
    return true if arg is an accpeted frequency

    :type asp: str
    :param asp: any accpeted frequency str

    :rtype: boolean
    :return: return true if arg is an accpeted frequency
    """
    return asp in ALL_ASPECTS or asp is None


def is_supported_crawler(cr):
    """
    return true if arg is an supported crawler

    :type cr: str
    :param cr: any accpeted crawler str

    :rtype: boolean
    :return: return true if arg is an accpeted crawler
    """
    return cr in ALL_CRALWERS or cr is None


# def is_search_types(cr):
#     return cr in ALL_SEARCH_TYPES

def get_respond_type_when_crawler_is_all(cr):
    """
    return list of crawler's respond type when arg == 'all' else output arg without change

    :param cr: str
    :param cr: any accepted crawler

    :return: list of str
    :return: list of crawler name
    """
    if cr == 'reddit':
        search_types = ALL_REDDIT_SEARCH_TYPE
    if cr == 'twitter':
        search_types = search_types, ALL_TWITTER_SEARCH_TYPE

    return search_types


@app.route("/", methods=['GET'])
def index():
    """
    prepared specified input parameters and return all retirieved data in database in json format

    :rtype:  json
    :return: all retrieved data in database
    """

    crawlers = request.args.get('crawlers')
    since = request.args.get('since')
    until = request.args.get('until')
    # after =  request.args.get('after')
    aspects = request.args.get('aspects')
    search_types = request.args.get('search_types')
    frequency = request.args.get('frequency')
    fields = request.args.get('fields')

    if aspects is None:
        aspects = 'all'

    if fields is None:
        fields = 'all'

    if frequency is None:
        frequency = 'day'

    if crawlers is None:
        crawlers = 'all'

    def is_reddit_search_type(s):
        return s in ALL_REDDIT_SEARCH_TYPE or s == 'all'

    def is_twitter_search_type(s):
        return s in ALL_TWITTER_SEARCH_TYPE or s == 'all'

    def ensure_compatiblity_of_search_types_and_crawlers(c, st, f):
        if st is None:
            st = 'all'
        if f is None:
            f = 'all'
        search_types_split = st.split(',')
        fields_split = f.split(',')
        if c == 'reddit':
            for i in search_types_split:
                assert is_reddit_search_type(i)
            for i in fields_split:
                assert is_reddit_fields(i)
            return [c], search_types_split, fields_split
        elif c == 'twitter':
            for i in search_types_split:
                assert is_twitter_search_type(i)
            for i in fields_split:
                assert is_twitter_fields(i)
            return [c], search_types_split, fields_split
        else:
            crawler_split = c.split(',')
            if len(crawler_split) == len(ALL_CRALWERS):
                for i in crawler_split:
                    assert is_supported_crawler(i)

                return ['all'], ['all'], ['all']
            else:
                raise ValueError

    if crawlers != 'all' and crawlers is not None:
        crawlers, search_types, fields = ensure_compatiblity_of_search_types_and_crawlers(
            crawlers, search_types, fields)
    elif crawlers == 'all':
        search_types = ['all']
        fields = ['all']
    elif crawlers is None:
        crawlers = ['all']
        search_types = ['all']
        fields = ['all']
    else:
        raise ValueError

    # def ensure_compatibility_of_fields_and_crawler(cr, f):
    #     if cr[0] == 'all'

    def convert_to_common_type(args, all_keywords=None, accept_all=True):
        if accept_all:
            assert all_keywords is not None, ''
        else:
            assert all_keywords is None, ''

        if args is None:
            return [None]
        if accept_all:
            args = args if isinstance(args, list) else args.split(',')
            if len(args) == 1 and args[0] == 'all':
                return all_keywords
            else:
                return args
        else:
            return args.split(',')

    crawlers = convert_to_common_type(crawlers, ALL_CRALWERS)
    aspects = convert_to_common_type(aspects, ALL_ASPECTS)
    since = convert_to_common_type(since, accept_all=False)
    until = convert_to_common_type(until, accept_all=False)
    frequency = convert_to_common_type(frequency, accept_all=False)
    # fields = convert_to_common_type(fields, accept_all=False)

    for aspect in aspects:
        assert is_supported_aspect(aspect)

    if since[0] is not None:
        assert is_date(since[0]) and len(since) == 1
        since_datetime = [datetime.datetime.strptime(since[0], DATEFORMAT)]
    else:
        since_datetime = since

    if until[0] is not None or until[0] == 'all':
        assert is_date(until[0]) and len(until) == 1

        until_datetime = [datetime.datetime.strptime(until[0], DATEFORMAT)]
    else:
        until_datetime = until

    assert is_supported_frequency(frequency[0])

    api_manager = APIManager(aspects, crawlers, since_datetime, until_datetime,
                             frequency, search_types, fields)

    return api_manager.get_all_retrived_data()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='127.0.0.1', port=5501, debug=True)
