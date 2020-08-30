import datetime
import os
import pathlib
import sqlite3
from typing import Dict
from typing import List
from typing import Optional
import pandas as pd

ALL_ASPECTS = ['work_from_home', 'social_distance',
               'corona', 'reopen', 'lockdown']
ALL_CRALWERS = ['twitter', 'reddit']
ALL_FREQUENCY = ['day']
ALL_REDDIT_SEARCH_TYPE = ['comment', 'submission']
ALL_TWITTER_SEARCH_TYPE = ['data_tweet']


def get_all_file_path() -> List[pathlib.Path]:
    reddit_path = pathlib.Path(
        r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data\RedditCrawler')
    twitter_path = pathlib.Path(
        r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data\TwitterCrawler')
    # raise NotImplementedError
    return [reddit_path, twitter_path]


def get_all_file_for_reddit(all_data_path: List[pathlib.Path]) -> Optional[
    List[pathlib.Path]]:
    return get_all_file_for_crawler(all_data_path, 'reddit', ALL_ASPECTS,
                                    ALL_REDDIT_SEARCH_TYPE)


def get_all_file_for_twitter(all_data_path: List[pathlib.Path]) -> Optional[
    List[pathlib.Path]]:
    return get_all_file_for_crawler(all_data_path, 'twitter', ALL_ASPECTS,
                                    ALL_TWITTER_SEARCH_TYPE)


def get_all_file_for_crawler(all_data_path: List[pathlib.Path], crawler: str,
                             aspect: List[str], search_types: List[str]) -> \
        Optional[List[pathlib.Path]]:
    all_files = []
    if crawler == 'reddit':
        all_reddit_files = []
        for i in all_data_path:
            for (dirpath, dirnames, filenames) in os.walk(i):
                # print(dirpath, dirnames)
                x = dirpath.split('\\')[-1]
                y = dirpath.split('\\')[-3]
                # if x in ['comment']:
                if x in search_types and y in aspect:
                    for (dirpath1, dirnames1, filenames1) in os.walk(
                            pathlib.Path(dirpath)):
                        for file in filenames1:
                            all_reddit_files.append(
                                pathlib.Path(dirpath1) / file)
        all_files.extend(all_reddit_files)

    if crawler == 'twitter':
        all_twitter_files = []
        for i in all_data_path:
            for (dirpath, dirnames, filenames) in os.walk(i):
                # print(dirpath, dirnames)
                x = dirpath.split('\\')[-1]
                y = dirpath.split('\\')[-3]
                # if x in ['comment']:
                if x in search_types and y in aspect:
                    for (dirpath1, dirnames1, filenames1) in os.walk(
                            pathlib.Path(dirpath)):
                        for file in filenames1:
                            all_twitter_files.append(
                                pathlib.Path(dirpath1) / file)
        all_files.extend(all_twitter_files)

    return all_files


def get_all_file(all_data_path: List[pathlib.Path], crawler: str) -> Dict:
    if crawler == 'reddit':
        all_reddit_files = get_all_file_for_reddit(all_data_path)
        return {'all_reddit_files': all_reddit_files}
    elif crawler == 'twitter':
        all_twitter_files = get_all_file_for_twitter(all_data_path)
        return {'all_twitter_files': all_twitter_files}
    else:
        raise ValueError


def get_all_data_from_files(all_files: Dict, crawler: str) -> Dict:
    # all_data_from_a_file

    def _get_all_data_from_a_file(file):
        import pickle
        retrieved_data_from_a_file = pickle.load(open(file, 'rb'))

        return retrieved_data_from_a_file

    if crawler == 'reddit':
        all_crawler_search_type =  ALL_REDDIT_SEARCH_TYPE
    elif crawler == 'twitter':
        all_crawler_search_type = ALL_TWITTER_SEARCH_TYPE
    else:
        raise ValueError

    all_retrieved_data: List = []
    for _, files_from_a_crawler in all_files.items():
        for file in files_from_a_crawler:
            retrieved_data_from_a_file = _get_all_data_from_a_file(file)

            def _get_data_from_folder():
                x = str(file).split('\\')
                tmp = {}
                if x[-3] in all_crawler_search_type:
                    tmp.update({'search_type': x[-3]})
                else:
                    raise ValueError()

                # # OPTIMIZE: I should check whether folder name is an acceptable value
                # if True:
                #     tmp.update({'collection_name':x[-4]})

                return {'data': tmp}

            retrieved_data_from_path_foler = _get_data_from_folder()
            all_retrieved_data.append(
                {'data_from_a_file': retrieved_data_from_a_file,
                 'data_from_folder_path': retrieved_data_from_path_foler})

    def _convert_to_output_format() -> Dict:
        if crawler == 'reddit':
            selected_data_keys: List[str] = ['body', 'title', 'created_utc',
                                             'sentiment',
                                             'subreddit', 'id', 'link_id',
                                             'parent_id', 'sentiment']
            selected_metadata_keys: List[str] = ['frequency', 'aspect']

            all_reddit_retrieved_data = []

            for data_from_file_and_folder in all_retrieved_data:
                i = data_from_file_and_folder['data_from_a_file']
                j = data_from_file_and_folder['data_from_folder_path']

                aggs, data, metadata = i
                # each_reddit_aggs = { key: i[key] for key in aggs }
                each_reddit_metadata = {key: i[metadata][key] for key in
                                        i[metadata] if
                                        key in selected_metadata_keys}
                for ind in range(len(i[data])):
                    tmp = {key: i[data][ind][key] for key in i[data][ind]
                                        if key in selected_data_keys}
                    all_reddit_retrieved_data.append({**tmp, **each_reddit_metadata, **j['data'] })

                # all_reddit_retrieved_data.append(
                #     {**each_reddit_data, **each_reddit_metadata, **j['data']})

            def check_if_aspect_has_no_duplicate(tmp: Dict) -> Dict:
                tmp_df = pd.DataFrame(tmp)
                tmp_dict: Dict = {}
                tmp_dict = tmp_df.drop_duplicates(subset=['id', 'aspect']).to_dict('record')
                return tmp_dict

            # all_reddit_retrieved_data_df = pd.DataFrame(all_reddit_retrieved_data)
            all_reddit_retrieved_data: Dict = check_if_aspect_has_no_duplicate(all_reddit_retrieved_data)
            # all_reddit_retrieved_data = all_reddit_retrieved_data_df.to_dict('record')

            return_data_no_dubplicate: Dict = {'reddit': all_reddit_retrieved_data}

            return return_data_no_dubplicate
            # import pandas as pd
            # all_reddit_retrieved_data_pd = pd.DataFrame.from_dict(all_reddit_retrieved_data)

        elif crawler == 'twitter':
            selected_data_keys: List[str] = ['text', 'id', 'date',
                                             'sentiment']
            selected_metadata_keys: List[str] = ['frequency', 'aspect']

            all_twitter_retrieved_data = []

            acc = []
            for data_from_file_and_folder in all_retrieved_data:
                i = data_from_file_and_folder['data_from_a_file']
                j = data_from_file_and_folder['data_from_folder_path']

                data, aggs, metadata = i
                # each_reddit_aggs = { key: i[key] for key in aggs }
                each_twitter_metadata = {key: i[metadata][key] for key in
                                        i[metadata] if
                                        key in selected_metadata_keys}

                for ind in range(len(i['data'])):
                    tmp = {key: i[data][ind][key] for key in i[data][ind]
                                             if key in selected_data_keys}
                    for  d,y in tmp.items():
                        if d == 'id':
                            acc.append(y) 
                    all_twitter_retrieved_data.append({**tmp, **each_twitter_metadata, **j['data']})

            returned_data: Dict = {'twitter': all_twitter_retrieved_data}
            return returned_data
            # _convert_to_pandas()
        else:
            raise ValueError()

    returned_data: Dict = _convert_to_output_format()

    return returned_data


class SocialMediaDatabase():
    def __init__(self, dbfile: str, data: Dict):

        self.conn = self._create_connection(dbfile)
        # self._get_all_data_from_sqlite()

        if dbfile == 'reddit_database':
            self.conn.cursor().execute("DROP table if exists reddit")
            self._create_table_reddit()

            for i in data['reddit']:
                self._insert_data_to_database('reddit', **i)

        elif dbfile == 'twitter_database':
            self.conn.cursor().execute("DROP table if exists twitter")
            self._create_table_twitter()

            for i in data['twitter']:
                self._insert_data_to_database('twitter', **i)
        else:
            raise ValueError

        self.conn.commit()
        self.conn.close()

    def _get_all_data_from_sqlite(self):
        cur = self.conn.cursor()
        cur.execute("select * from reddit")
        r = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        print(r)

    def _create_connection(self, dbfile: str) -> sqlite3.Connection:
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            return conn
        except ValueError as e:
            raise ValueError(e)

    def _create_table_reddit(self) -> str:

        query = """ CREATE TABLE IF NOT EXISTS reddit (
                                    crawler STRING
                                    , created_utc str
                                    , body STRING
                                    , title STRING
                                    , search_type STRING
                                    , aspect STRING
                                    , frequency STRING
                                    , sentiment double
                                    , subreddit STRING
                                    , link_id STRING 
                                    , id STRING 
                                    , parent_id STRING 
                                    , UNIQUE (id, aspect)
                                ); 
                                """

        c = self.conn.cursor()
        c.execute(query)

    def _create_table_twitter(self) -> str:

        # text
        # id, date, sentiment, frequency, aspect
        query = """ CREATE TABLE IF NOT EXISTS twitter (
                                    crawler STRING
                                    , date str
                                    , text STRING
                                    , search_type STRING
                                    , aspect STRING
                                    , frequency STRING
                                    , sentiment double
                                    , id STRING 
                                    , UNIQUE (id , aspect)
                                ); 
                                """

        c = self.conn.cursor()
        c.execute(query)


    def _reddit_insert_query(self, **kwargs):

        columns_to_be_inserted: List[str] = []
        value_to_be_inserted: List[str] = []

        for k, v in kwargs.items():
            columns_to_be_inserted.append(k)
            value_to_be_inserted.append(v)

        def _convert_value_to_correct_type():
            new_val = []
            new_col = []
            for i, (v, k) in enumerate(
                    zip(value_to_be_inserted, columns_to_be_inserted)):
                if not isinstance(v,
                                  str):
                    if v is None:
                        value_to_be_inserted[i] = 'None'
                        continue
                    else:
                        value_to_be_inserted[i] = str(v)
                        value_to_be_inserted[i] = value_to_be_inserted[
                            i].replace('"', "'")
                else:
                    value_to_be_inserted[i] = v
                    value_to_be_inserted[i] = value_to_be_inserted[i].replace('"',
                                                                              "'")

                if value_to_be_inserted[i] is not None:
                    if k != 'sentiment' and k != 'created_utc':
                        tmp = value_to_be_inserted[i]
                        value_to_be_inserted[i] = '"' + tmp + '"'
                new_val.append(value_to_be_inserted[i])
                new_col.append(columns_to_be_inserted[i])

            return new_val, new_col

        value_to_be_inserted, columns_to_be_inserted = _convert_value_to_correct_type()

        return """INSERT INTO reddit ({columns_to_be_inserted})
        VALUES({value_to_be_inserted});
        """.format(columns_to_be_inserted=','.join(columns_to_be_inserted),
                   value_to_be_inserted=','.join(value_to_be_inserted))

    def _twitter_insert_query(self, **kwargs):

        columns_to_be_inserted: List[str] = []
        value_to_be_inserted: List[str] = []

        for k, v in kwargs.items():
            columns_to_be_inserted.append(k)
            value_to_be_inserted.append(v)

        def _convert_value_to_correct_type():
            new_val = []
            new_col = []
            for i, (v, k) in enumerate(
                    zip(value_to_be_inserted, columns_to_be_inserted)):
                if not isinstance(v,
                                  str):
                    if v is None:
                        value_to_be_inserted[i] = 'None'
                        continue
                    else:
                        value_to_be_inserted[i] = str(v)
                        value_to_be_inserted[i] = value_to_be_inserted[
                            i].replace('"', "'")
                else:
                    value_to_be_inserted[i] = v
                    value_to_be_inserted[i] = value_to_be_inserted[i].replace('"',
                                                                              "'")

                if value_to_be_inserted[i] is not None:
                    if k != 'sentiment' and k != 'created_utc':
                        tmp = value_to_be_inserted[i]
                        value_to_be_inserted[i] = '"' + tmp + '"'
                new_val.append(value_to_be_inserted[i])
                new_col.append(columns_to_be_inserted[i])

            return new_val, new_col

        value_to_be_inserted, columns_to_be_inserted = _convert_value_to_correct_type()

        return """INSERT INTO twitter ({columns_to_be_inserted})
        VALUES({value_to_be_inserted});
        """.format(columns_to_be_inserted=','.join(columns_to_be_inserted),
                   value_to_be_inserted=','.join(value_to_be_inserted))

    def _insert_reddit_data_to_database(self, reddit_query: str):
        c = self.conn.cursor()
        c.execute(reddit_query)

    def _insert_twitter_data_to_database(self, twitter_query: str):
        c = self.conn.cursor()
        c.execute(twitter_query)


    def _insert_data_to_database(self, crawler: str, **kwargs):
        if crawler == 'reddit':
            # all_reddit_retrieved_data.append(
            #     {**each_reddit_data, **each_reddit_metadata, **j['data']})
            kwargs = {**kwargs, 'crawler': crawler}
            self._insert_reddit_data_to_database(
                self._reddit_insert_query(**kwargs))
        elif crawler == 'twitter':
            self._insert_twitter_data_to_database(
                self._twitter_insert_query(**kwargs))
        else:
            raise ValueError()


def add_data(conn, add_data_sql):
    try:
        c = conn.cursor()
        c.execute(add_data_sql)
    except ValueError as e:

        raise ValueError(e)

        pass


if __name__ == "__main__":

    all_data_path = get_all_file_path()
    all_files = get_all_file(all_data_path, 'reddit')
    all_data = get_all_data_from_files(all_files, 'reddit')
    SocialMediaDatabase('reddit_database', all_data)

    # all_data_path = get_all_file_path()
    # all_files = get_all_file(all_data_path, 'twitter')
    # all_data = get_all_data_from_files(all_files, 'twitter')
    # SocialMediaDatabase('twitter_database', all_data)

    print('complete running..')
