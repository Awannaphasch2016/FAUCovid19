# -*- coding: utf-8 -*-

"""Update crawled social media data with sqlite3 database."""

import os
import pathlib
import sqlite3
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd  # type: ignore

from credentials import MYSQL_PASSWORD
from credentials import MYSQL_USERNAME
from global_parameters import ALL_ASPECTS
from global_parameters import ALL_CRAWLERS
from global_parameters import ALL_REDDIT_FEILDS
from global_parameters import ALL_REDDIT_SEARCH_TYPES
from global_parameters import ALL_TWITTER_SEARCH_TYPES
from global_parameters import DATABASE_TYPE
from global_parameters import MYSQL_HOST
from global_parameters import MYSQL_PORT
from global_parameters import REDDIT_DATABASE
from src.Sources.Preparations.Data import get_keywords_collections
from src.Sources.Preparations.Data.social_media_crawler import \
    _get_crawler_tags_words
from src.Utilities import Frequency
from src.Utilities import MyLogger

LOGGER = MyLogger()
PROGRAM_LOGGER = LOGGER.program_logger

sys.path.insert(0, str(pathlib.Path(os.getcwd()).parent.parent.parent.parent))

from global_parameters import BASE_DIR  # noqa: E402


def get_all_file_path() -> List[pathlib.Path]:
    """
    Return all available social media date distinct root path.

    :rtype: list of pathlib.Path
    :return: list of path to crawler output data
    """
    reddit_path = pathlib.Path(BASE_DIR) / pathlib.Path(
        r"Outputs\Data\RedditCrawler",
    )
    twitter_path = pathlib.Path(BASE_DIR) / pathlib.Path(
        r"Outputs\Data\TwitterCrawler",
    )
    # raise NotImplementedError
    return [reddit_path, twitter_path]


def get_all_file_for_reddit(
        all_data_path: List[pathlib.Path],
) -> Optional[List[pathlib.Path]]:  # noqa: E125
    """
    Return list of file path contained reddit output date.

    :type all_data_path: list of pathlib.Path
    :param all_data_path: all reddit output data folder path

    :rtype: list of pathlib.Path
    :return: list of file path contained reddit output data
    """
    return get_all_file_for_crawler(
        all_data_path,
        "reddit",
        ALL_ASPECTS,
        ALL_REDDIT_SEARCH_TYPES,
    )


def get_all_file_for_twitter(
        all_data_path: List[pathlib.Path],
) -> Optional[List[pathlib.Path]]:  # noqa: E125
    """
    Return list of file path contained twitter output data.

    :type all_data_path: list of pathlib.Path
    :param all_data_path: all twitter output data folder path

    :rtype: list of pathlib.Path
    :return: list of file path contained twitter output data
    """
    return get_all_file_for_crawler(
        all_data_path,
        "twitter",
        ALL_ASPECTS,
        ALL_TWITTER_SEARCH_TYPES,
    )


def get_all_file_for_crawler(
        all_data_path: List[pathlib.Path],
        crawler: str,
        aspect: List[str],
        search_types: List[str],
) -> Optional[List[pathlib.Path]]:
    """Skipped summary.

    Prepared parameters + return list of file path contained a specified
    crawler output data.

    :type all_data_path: list of pathlib.Path
    :param all_data_path: all reddit output data folder path

    :param crawler: str
    :param crawler: crawler name

    :type aspect: Tags
    :param aspect: any specified aspect

    :type search_type: str
    :param search_type: desired search type by crawler

    :rtype: None or list of pathlib.Path
    :return: list of file path contained a specified crawler output data
    """
    all_files = []
    if crawler == "reddit":
        all_reddit_files = []
        for i in all_data_path:
            for (dirpath, _dirnames, _filenames) in os.walk(i):
                # print(dirpath, dirnames)
                x = dirpath.split("\\")[-1]
                y = dirpath.split("\\")[-3]
                # if x in ['comment']:
                if x in search_types and y in aspect:
                    for (dirpath1, _dirnames1, filenames1) in os.walk(
                            pathlib.Path(dirpath),
                    ):
                        for file in filenames1:
                            all_reddit_files.append(
                                pathlib.Path(dirpath1) / file,
                            )
        all_files.extend(all_reddit_files)

    if crawler == "twitter":
        all_twitter_files = []
        for i in all_data_path:
            for (dirpath, _dirnames, _filenames) in os.walk(i):
                # print(dirpath, dirnames)
                x = dirpath.split("\\")[-1]
                y = dirpath.split("\\")[-3]
                # if x in ['comment']:
                if x in search_types and y in aspect:
                    for (dirpath1, _dirnames1, filenames1) in os.walk(
                            pathlib.Path(dirpath),
                    ):
                        for file in filenames1:
                            all_twitter_files.append(
                                pathlib.Path(dirpath1) / file,
                            )
        all_files.extend(all_twitter_files)

    return all_files


def get_all_file(all_data_path: List[pathlib.Path], crawler: str) -> Dict:
    """
    Return list of file path contained a specified crawler output data.

    :type all_data_path: list of pathlib.Path
    :param all_data_path: all reddit output data folder path

    :param crawler: str
    :param crawler: crawler name


    :rtype: dict containing a specified crawler file path
    :return: dict of file path contained reddit output data
    """
    if crawler == "reddit":
        all_reddit_files = get_all_file_for_reddit(all_data_path)
        return {"all_reddit_files": all_reddit_files}
    elif crawler == "twitter":
        all_twitter_files = get_all_file_for_twitter(all_data_path)
        return {"all_twitter_files": all_twitter_files}
    else:
        raise ValueError


# OPTIMIZE: I need to refactor this code into get_all_data_from_reddit_file()
#  and get_all_data_from_twitter_file()
def get_all_data_from_files(all_files: Dict, crawler: str) -> Dict:
    """Skipped summary.


    Get all data from file and folder_path (name extracted from folder path
        which is not provided by the output from api). Output dictionary
        will have keys of 1. data 2. metadata.
        Note: it is worth nothing that data extracted from folder is a type
            of data's keys.

    :type all_files: Dict
    :param all_files: all file paths to crawler's output data

    :type crawler: str
    :param crawler: crawler_name

    :rtype: Dict
    :return: dict of all returned data from specified crawler's database
    """

    # all_data_from_a_file
    def _get_all_data_from_a_file(file):
        import pickle

        retrieved_data_from_a_file = pickle.load(open(file, "rb"))

        return retrieved_data_from_a_file

    if crawler == "reddit":
        all_crawler_search_type = ALL_REDDIT_SEARCH_TYPES
    elif crawler == "twitter":
        all_crawler_search_type = ALL_TWITTER_SEARCH_TYPES
    else:
        raise ValueError

    all_retrieved_data: List = []
    for _, files_from_a_crawler in all_files.items():
        for file in files_from_a_crawler:
            retrieved_data_from_a_file = _get_all_data_from_a_file(file)

            def _get_data_from_folder():
                x = str(file).split("\\")
                tmp = {}
                if x[-3] in all_crawler_search_type:
                    tmp.update({"search_type": x[-3]})
                else:
                    raise ValueError()

                # OPTIMIZE: I should check whether folder name is an
                #   acceptable value
                # if True:
                #     tmp.update({'collection_name':x[-4]})

                return {"data": tmp}

            retrieved_data_from_path_foler = _get_data_from_folder()
            all_retrieved_data.append(
                {
                    "data_from_a_file": retrieved_data_from_a_file,
                    "data_from_folder_path": retrieved_data_from_path_foler,
                },
            )

    def _convert_to_output_format() -> Dict:
        selected_data_keys: List[str] = []
        selected_metadata_keys: List[str]
        if crawler == "reddit":
            selected_data_keys = [
                "body",
                "title",
                "created_utc",
                "sentiment",
                "subreddit",
                "id",
                "link_id",
                "parent_id",
                "sentiment",
            ]
            selected_metadata_keys = ["frequency", "aspect"]

            all_reddit_retrieved_data = []

            for data_from_file_and_folder in all_retrieved_data:
                i = data_from_file_and_folder["data_from_a_file"]
                j = data_from_file_and_folder["data_from_folder_path"]

                each_reddit_metadata: Dict = {}

                # NOTE: reddit_stream_data only have data keys. I have to
                #   implemet for aggs and metadata
                try:
                    aggs, data, metadata = i
                    # each_reddit_aggs = { key: i[key] for key in aggs }
                    each_reddit_metadata = {
                        key: i[metadata][key]
                        for key in i[metadata]
                        if key in selected_metadata_keys
                    }
                except:
                    data = i

                for ind in range(len(i['data'])):
                    tmp = {
                        key: i['data'][ind][key]
                        for key in i['data'][ind]
                        if key in selected_data_keys
                    }
                    all_reddit_retrieved_data.append(
                        {**tmp, **each_reddit_metadata, **j["data"]},
                    )

                # all_reddit_retrieved_data.append(
                #     {**each_reddit_data, **each_reddit_metadata,
                #      **j['data']})

            def check_if_aspect_has_no_duplicate(tmp: List[Dict]) -> Dict:
                tmp_df = pd.DataFrame(tmp)
                tmp_dict: Dict = {}
                tmp_dict = tmp_df.drop_duplicates(
                    subset=["id", "aspect"],
                ).to_dict("record")
                return tmp_dict

            # all_reddit_retrieved_data_df = pd.DataFrame(
            #     all_reddit_retrieved_data)
            all_reddit_retrieved_data_: Dict = \
                check_if_aspect_has_no_duplicate(
                    all_reddit_retrieved_data,
                )
            # all_reddit_retrieved_data = all_reddit_retrieved_data_df.to_dict(
            #     'record')

            return_data_no_dubplicate: Dict = {
                "reddit": all_reddit_retrieved_data_,
            }

            return return_data_no_dubplicate
            # import pandas as pd
            # all_reddit_retrieved_data_pd = pd.DataFrame.from_dict(
            #     all_reddit_retrieved_data)

        elif crawler == "twitter":
            selected_data_keys = ["text", "id", "date", "sentiment"]
            selected_metadata_keys = ["frequency", "aspect"]

            all_twitter_retrieved_data = []

            acc = []
            for data_from_file_and_folder in all_retrieved_data:
                i = data_from_file_and_folder["data_from_a_file"]
                j = data_from_file_and_folder["data_from_folder_path"]

                data, aggs, metadata = i
                # each_reddit_aggs = { key: i[key] for key in aggs }
                each_twitter_metadata = {
                    key: i[metadata][key]
                    for key in i[metadata]
                    if key in selected_metadata_keys
                }

                for ind in range(len(i["data"])):
                    tmp = {
                        key: i[data][ind][key]
                        for key in i[data][ind]
                        if key in selected_data_keys
                    }
                    for d, y in tmp.items():
                        if d == "id":
                            acc.append(y)
                    all_twitter_retrieved_data.append(
                        {**tmp, **each_twitter_metadata, **j["data"]},
                    )

            returned_data: Dict = {"twitter": all_twitter_retrieved_data}
            return returned_data
            # _convert_to_pandas()
        else:
            raise ValueError()

    returned_data: Dict = _convert_to_output_format()

    return returned_data


class SocialMediaDatabase:
    """Skipped summary.

    Prepare data to create table and insert data into specified crawler
    database.
    """

    def __init__(
            self, dbfile_path: str, data: Dict,
            update_stream_data: bool = True):
        """Skipped summary.


        :type update_stream_data: bool
        :param update_stream_data: if true, using update
            procedure for stream_data to data base else using update
            procedure for cralwed_data (not stream data)


        """

        self.count = 0
        dbfile_path = dbfile_path.replace('\\', '/')
        dbfile = dbfile_path.split("/")[-1]
        self.dbfile = dbfile
        self.data = data
        self.conn = self._create_connection(dbfile_path)
        # self._get_all_data_from_sqlite()
        self.update_stream_data: bool = update_stream_data
        self.update_to_database()

    # def _get_all_data_from_sqlite(self):
    #     """
    #     execute sql query to return all data from sqlite database
    #     :return:
    #     """
    #     cur = self.conn.cursor()
    #     cur.execute("select * from reddit")
    #     r = [dict((cur.description[i][0], value) \
    #               for i, value in enumerate(row)) for row in cur.fetchall()]
    #     print(r)

    def _create_connection(self, dbfile: str) -> sqlite3.Connection:
        """Skipped summary.

        Create a database connection to the SQLite database specified by
        db_file.

        :type db_file: str
        :param db_file: database file

        :rtype: sqlite3.Connection
        :return: Connection object
        """
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            return conn
        except ValueError as e:
            raise ValueError(e)

    def _create_table_reddit(self) -> None:
        """Run query to create reddit schema in twitter database."""
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

    def _create_table_reddit_stream_data(self) -> None:
        """
        Run query to create twitter schema in reddit stream data database.
        """
        try:
            self.database_name = 'reddit_stream'
            query: str = f""" CREATE TABLE IF NOT EXISTS {self.database_name} (
                                        author STRING
                                        , body STRING
                                        , body_html STRING
                                        , created_utc double
                                        , edited BOOL
                                        , id STRING
                                        , is_submitter BOOL
                                        , link_id STRING
                                        , parent_id STRING
                                        , permalink STRING
                                        , replies STRING
                                        , score int
                                        , stickied BOOL
                                        , submission STRING
                                        , subreddit STRING
                                        , subreddit_id STRING
                                        , sentiment double
                                        , UNIQUE (id)
                                    );
                                    """

            c = self.conn.cursor()
            c.execute(query)

        except BaseException as e:
            PROGRAM_LOGGER. \
                error(
                f" {str(e)} occurs in"
                f" {self._create_table_reddit_stream_data().__name__}"
            )
            raise BaseException(e)

    def _create_table_twitter(self) -> None:
        """Run query to create twitter schema in twitter database."""
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
        """
        Return str of query to insert data into reddit database.

        :param kwargs: dict
        :param kwargs: dict of parameters

        :rtype: str
        :return: str of character to insert query to reddit
        """
        columns_to_be_inserted: List[str] = []
        value_to_be_inserted: List[str] = []

        for k, v in kwargs.items():
            columns_to_be_inserted.append(k)
            value_to_be_inserted.append(v)

        def _convert_value_to_correct_type():
            new_val = []
            new_col = []
            for i, (v, k) in enumerate(
                    zip(value_to_be_inserted, columns_to_be_inserted),
            ):
                if not isinstance(v, str):
                    if v is None:
                        value_to_be_inserted[i] = "None"
                        continue
                    else:
                        value_to_be_inserted[i] = str(v)
                        value_to_be_inserted[i] = \
                            value_to_be_inserted[i].replace('"', "'")
                else:
                    value_to_be_inserted[i] = v
                    value_to_be_inserted[i] = \
                        value_to_be_inserted[i].replace(
                            '"',
                            "'",
                        )

                if value_to_be_inserted[i] is not None:
                    if k != "sentiment" and k != "created_utc":
                        tmp = value_to_be_inserted[i]
                        value_to_be_inserted[i] = '"' + tmp + '"'
                new_val.append(value_to_be_inserted[i])
                new_col.append(columns_to_be_inserted[i])

            return new_val, new_col

        (
            value_to_be_inserted,
            columns_to_be_inserted,
        ) = _convert_value_to_correct_type()

        columns_to_be_inserted = ",".join(columns_to_be_inserted)
        value_to_be_inserted = ",".join(value_to_be_inserted)

        return f"""INSERT INTO reddit ({columns_to_be_inserted})
        VALUES({value_to_be_inserted});
        """

    def _reddit_insert_query_for_stream_data(self, **kwargs):
        """
        Return str of query to insert data into reddit database.

        :param kwargs: dict
        :param kwargs: dict of parameters

        :rtype: str
        :return: str of character to insert query to reddit
        """
        try:
            columns_to_be_inserted: List[str] = []
            value_to_be_inserted: List[str] = []

            columns_and_value_tuple_dict: \
                Dict[str, Any] = self.data['reddit'][0]

            def _convert_value_to_sqlite_type() -> Dict:
                tmp: Dict = {}
                for i, j in columns_and_value_tuple_dict.items():
                    tmp[i] = str(j)

                for i, j in tmp.items():
                    columns_and_value_tuple_dict[i] = j

                return columns_and_value_tuple_dict

            columns_and_value_tuple_dict = _convert_value_to_sqlite_type()

            columns_to_be_inserted: List[str] = \
                list(columns_and_value_tuple_dict.keys())

            value_to_be_inserted: List[str] = \
                list(
                    map(
                        lambda x: '"' + x.replace('"', "'") + '"',
                        list(columns_and_value_tuple_dict.values())
                    )
                )

            columns_to_be_inserted = ",".join(columns_to_be_inserted)
            value_to_be_inserted = ",".join(value_to_be_inserted)

        except Exception as e:
            PROGRAM_LOGGER.error(
                f'There is error occurs in '
                f'{self._insert_reddit_stream_data_to_database().__name__}'
                f' : error is `{e}`')
            raise Exception(e)

        query: str = f""" INSERT INTO {self.database_name} 
            ({columns_to_be_inserted})
            VALUES({value_to_be_inserted});
            """
        PROGRAM_LOGGER.info(f'{query}')

        return query

    def _twitter_insert_query(self, **kwargs) -> str:
        """
        Return str of query to insert data into twitter database.

        :param kwargs: dict
        :param kwargs: dict of parameters

        :rtype: str
        :return: str of character to insert query to twitter
        """
        columns_to_be_inserted: List[str] = []
        value_to_be_inserted: List[str] = []

        for k, v in kwargs.items():
            columns_to_be_inserted.append(k)
            value_to_be_inserted.append(v)

        def _convert_value_to_correct_type():
            new_val = []
            new_col = []
            for i, (v, k) in enumerate(
                    zip(value_to_be_inserted, columns_to_be_inserted),
            ):
                if not isinstance(v, str):
                    if v is None:
                        value_to_be_inserted[i] = "None"
                        continue
                    else:
                        value_to_be_inserted[i] = str(v)
                        value_to_be_inserted[i] = value_to_be_inserted[
                            i
                        ].replace('"', "'")
                else:
                    value_to_be_inserted[i] = v
                    value_to_be_inserted[i] = value_to_be_inserted[i].replace(
                        '"',
                        "'",
                    )

                if value_to_be_inserted[i] is not None:
                    if k != "sentiment" and k != "created_utc":
                        tmp = value_to_be_inserted[i]
                        value_to_be_inserted[i] = '"' + tmp + '"'
                new_val.append(value_to_be_inserted[i])
                new_col.append(columns_to_be_inserted[i])

            return new_val, new_col

        (
            value_to_be_inserted,
            columns_to_be_inserted,
        ) = _convert_value_to_correct_type()

        columns_to_be_inserted_ = ",".join(columns_to_be_inserted)
        value_to_be_inserted_ = ",".join(value_to_be_inserted)

        return f"""INSERT INTO twitter ({columns_to_be_inserted_})
        VALUES({value_to_be_inserted_});
        """

    def _insert_reddit_data_to_database(self, reddit_query: str):
        """
        Execute reddit insert query.

        :type twitter_query: str
        :param twitter_query: str of character to insert query to twitter
        """
        c = self.conn.cursor()
        c.execute(reddit_query)

    def _insert_reddit_stream_data_to_database(self, reddit_query: str):
        """
        Execute reddit insert query.

        :type twitter_query: str
        :param twitter_query: str of character to insert query to twitter
        """
        try:
            c = self.conn.cursor()
            c.execute(reddit_query)

        except sqlite3.OperationalError as e:
            self.count += 1

            PROGRAM_LOGGER.error(
                f'There is error occurs in '
                f'{self._reddit_insert_query_for_stream_data.__name__}'
                f' : error is `{e}`')
            PROGRAM_LOGGER.error(f"There are {self.count} faulty data "
                                 f"response.")
            raise Exception(e)

        except Exception as e:
            PROGRAM_LOGGER.error(
                f'There is error occurs in '
                f'{self._insert_reddit_stream_data_to_database.__name__}'
                f' : error is `{e}`')
            raise e

    def _insert_twitter_data_to_database(self, twitter_query: str):
        """
        Execute twitter insert query.

        :type twitter_query: str
        :param twitter_query: str of character to insert query to twitter
        """
        c = self.conn.cursor()
        c.execute(twitter_query)

    def _insert_data_to_database(self, crawler: str, **kwargs):
        """
        Insert data into a specified crawler database.

        :type crawler: str
        :param crawler: crawler name

        :param kwargs: dict
        :param kwargs: dict of parameters
        """
        if crawler == "reddit":
            # all_reddit_retrieved_data.append(
            #     {**each_reddit_data, **each_reddit_metadata, **j['data']})
            kwargs = {**kwargs, "crawler": crawler}
            try:
                self._insert_reddit_data_to_database(
                    self._reddit_insert_query(**kwargs),
                )
            except sqlite3.OperationalError as e:
                # BUG: value of setinment in 1 of all the data response
                #  is `nan`. Not sure why that is the case, but as of now,
                #  there is only 1 data response. so I just skipped them
                self.count += 1
                PROGRAM_LOGGER.error(
                    f'There is error occurs in '
                    f'{self._insert_data_to_database.__name__}'
                    f' : error is `{e}`')
                PROGRAM_LOGGER.error(f"There are {self.count} faulty data "
                                     f"response.")
            except Exception as e:
                raise e

        elif crawler == "twitter":
            self._insert_twitter_data_to_database(
                self._twitter_insert_query(**kwargs),
            )
        else:
            raise ValueError()

    def _insert_data_to_database_for_stream_data(self, crawler: str, **kwargs):
        """
        Insert data into a specified crawler database.

        :type crawler: str
        :param crawler: crawler name

        :param kwargs: dict
        :param kwargs: dict of parameters
        """
        if crawler == "reddit":
            kwargs = {**kwargs, "crawler": crawler}
            self._insert_reddit_stream_data_to_database(
                self._reddit_insert_query_for_stream_data(**kwargs),
            )

        elif crawler == "twitter":
            raise NotImplementedError('not yet implemenetd')
        else:
            raise ValueError()

    def update_to_database(self):
        if self.update_stream_data:
            self.update_to_database_for_stream_data()
        else:
            self.update_to_database_for_non_stream_data()

    def update_to_database_for_non_stream_data(self):

        if self.dbfile == "reddit_database.db":
            self.conn.cursor().execute("DROP table if exists reddit")
            self._create_table_reddit()

            for i in self.data["reddit"]:
                self._insert_data_to_database("reddit", **i)

        elif self.dbfile == "twitter_database.db":
            self.conn.cursor().execute("DROP table if exists twitter")
            self._create_table_twitter()

            for i in self.data["twitter"]:
                self._insert_data_to_database("twitter", **i)
        else:
            raise ValueError

        self.conn.commit()
        self.conn.close()
        print()

    def update_to_database_for_stream_data(self):

        if self.dbfile == "reddit_database.db":

            self._create_table_reddit_stream_data()

            for i in self.data['reddit']:
                self._insert_data_to_database_for_stream_data("reddit", **i)
        elif self.dbfile == "twitter_database.db":
            raise NotImplementedError
        else:
            raise ValueError

        self.conn.commit()
        self.conn.close()


# def add_data(conn, add_data_sql):
#     try:
#         c = conn.cursor()
#         c.execute(add_data_sql)
#     except ValueError as e:
#
#         raise ValueError(e)
#
#         pass

class RedditStream:
    def __init__(self, db_config: Dict,
                 db_type: str,
                 table_name='reddit_stream'):

        self.db_config = db_config
        self.db_type = db_type

        self.crawler_name = ALL_CRAWLERS[1]
        self.table_schema = self.get_table_schema_from_reddit_stream()
        self.aspect_database_name = ALL_CRAWLERS[3]
        # self.pull_data_from_sqlite3_reddit_stream_table()
        self.group_reddit_stream_data_into_aspect()
        self.insert_processed_data_to_reddit_database()

    def convert_reddit_stream_data_to_reddit_data(
            self,
            search_type: str,
            aspect_name: str,
            all_aspect_data_dict: Dict[str, Any],
            all_processed_data_as_input_reddit_table: List[
                Dict[
                    str,
                    Union[str, List[Dict[str, Any]]]
                ]
            ]
    ) -> Dict[
        str,
        Union[str, List[Dict[str, Any]]]
    ]:
        frequency: Frequency = 'stream'

        # def _get_keys_that_are_in_reddit_but_not_in_reddit_stream():
        #     column_in_reddit_stream = set(all_aspect_data_dict.keys())
        #     x = set(ALL_REDDIT_FEILDS).difference(column_in_reddit_stream)
        #     return x
        # keys_not_in_reddit_stream = \
        # _get_keys_that_are_in_reddit_but_not_in_reddit_stream()

        # all_processed_data_as_input_reddit_table.append({
        #     **all_aspect_data_dict,
        # })

        tmp: Dict = {
            **{'aspect': aspect_name},
            **{'crawler': self.crawler_name},
            **{'search_type': search_type},
            **{'frequency': frequency},
            **{'title': 'None'},
        }
        for i, j in all_aspect_data_dict.items():
            if i in ALL_REDDIT_FEILDS:
                tmp[i] = j
                all_processed_data_as_input_reddit_table.append(tmp)

        def _has_all_reddit_keys() -> bool \
                :
            return len(set(all_processed_data_as_input_reddit_table[-1].
                           keys()). \
                       symmetric_difference(ALL_REDDIT_FEILDS)) != 0

        if _has_all_reddit_keys():
            raise ValueError('some reddit columns are missing ')

        return all_processed_data_as_input_reddit_table

    def group_reddit_stream_data_into_aspect(self):

        self.group_reddit_stream_data_into_aspect_for_comment_search_type()

        # def convert_reddit_stream_data_to_reddit_data(self):
        #     pass

    def _create_connection(self, db_config: Dict) -> sqlite3.Connection:
        """Skipped summary.

        Create a database connection to the SQLite database specified by
        db_file.

        :type db_file: str
        :param db_file: database file

        :rtype: sqlite3.Connection
        :return: Connection object
        """
        conn = None
        try:
            if self.db_type == DATABASE_TYPE[0]:
                import sqlite3
                db_file = db_config['db_file']
                conn = sqlite3.connect(db_file)
            elif self.db_type == DATABASE_TYPE[1]:
                import mysql.connector
                # Connect to server
                conn = mysql.connector.connect(**db_config)
            else:
                raise ValueError
        except ValueError as e:
            raise ValueError(e)

        return conn

    def convert_reddit_stream_data_to_reddit_data_for_each_aspect(
            self,
            conn: Any,
            aspect_name: str) -> Tuple[str, ...]:

        (
            General,
            Country,
            Region,
            states_subreddit,
            social_distance_keywords,
            lockdown_keywords,
            work_from_home_keywords,
            covid_keywords,
            reopen_keywords,
        ) = get_keywords_collections(ALL_CRAWLERS[1])

        # =====================
        # == group data by aspect
        # =====================

        def execute_sqlite_query(aspect_name: str) -> List[Dict[str, Any]]:
            def get_subreddit_for_aspect() -> List[str]:
                return General + Country + Region + states_subreddit

            def get_keyword_for_aspect(aspect_name: str) -> List[str]:
                # VALIDATE: haven't test below paragraph
                tag_words = _get_crawler_tags_words(
                    crawler=ALL_CRAWLERS[1],
                    tag=aspect_name,
                    work_from_home_keywords=work_from_home_keywords,
                    lockdown_keywords=lockdown_keywords,
                    social_distance_keywords=social_distance_keywords,
                    corona_keywords=covid_keywords,
                    reopen_keywords=reopen_keywords,
                )
                return tag_words

            def get_all_data_for_aspect(
                    aspect_keywords: List[str],
            ) -> List[str]:
                if self.crawler_name != 'reddit':
                    raise ValueError

                all_aspect_subreddit_query = \
                    list(
                        map(
                            lambda x: "'" + x + "'",
                            aspect_subreddits,
                        )
                    )
                all_aspect_subreddit_query_str = ','.join(
                    all_aspect_subreddit_query)

                aspect_keywords_query: List[str] = \
                    list(map(
                        lambda x: "body LIKE '%" + x + "%'",
                        [i for i in aspect_keywords])
                    )
                aspect_keywords_query_str: str = ' OR '.join(
                    aspect_keywords_query)

                aspect_query = f"""
                    select *
                    from {self.aspect_database_name}
                    where subreddit in ({all_aspect_subreddit_query_str}) AND  
                    ({aspect_keywords_query_str})
                    ;
                    """

                def execute_sqlite_query(aspect_query: str) -> Tuple[str, ...]:
                    c = conn.cursor()
                    c.execute(aspect_query)
                    query_result = c.fetchall()

                    return query_result[0]

                # BUG: not sure why i can't return value from function
                query_result: Tuple[str, ...]
                query_result = execute_sqlite_query(aspect_query)

                return query_result

            aspect_subreddits: List[str] = get_subreddit_for_aspect()
            aspect_keywords: List[str] = get_keyword_for_aspect(aspect_name)
            all_aspect_data: Tuple[str, ...] = \
                get_all_data_for_aspect(
                    aspect_keywords,
                )

            return all_aspect_data

        all_aspect_data: Tuple[str, ...] = execute_sqlite_query(
            aspect_name)

        return all_aspect_data

    def group_reddit_stream_data_into_aspect_for_comment_search_type(
            self) -> Dict:

        # conn = self._create_connection(sqlite_file)
        conn = self._create_connection(self.db_config)
        all_processed_data_as_input_reddit_table: List[
            Dict[str, Union[str, List[Dict[str, Any]]]]
        ] = []

        for aspect_name in ALL_ASPECTS:
            all_aspect_data: List[Tuple[str, ...]] = \
                self. \
                    convert_reddit_stream_data_to_reddit_data_for_each_aspect(
                    conn,
                    aspect_name
                )
            all_aspect_data_dict: Dict[str, Any] = {
                i: j for (i, j)
                in zip(self.table_schema, all_aspect_data)
            }
            all_processed_data_as_input_reddit_table = \
                self.convert_reddit_stream_data_to_reddit_data(
                    'comment',
                    aspect_name,
                    all_aspect_data_dict,
                    all_processed_data_as_input_reddit_table,
                )
            print()

        conn.commit()
        conn.close()

        # self.all_aspect_data_dict = all_processed_data_as_input_reddit_table
        return all_processed_data_as_input_reddit_table

    def _reddit_insert_query(self, **kwargs):
        """
        Return str of query to insert data into reddit database.

        :param kwargs: dict
        :param kwargs: dict of parameters

        :rtype: str
        :return: str of character to insert query to reddit
        """
        columns_to_be_inserted: List[str] = []
        value_to_be_inserted: List[str] = []

        for k, v in kwargs.items():
            columns_to_be_inserted.append(k)
            value_to_be_inserted.append(v)

        def _convert_value_to_correct_type():
            new_val = []
            new_col = []
            for i, (v, k) in enumerate(
                    zip(value_to_be_inserted, columns_to_be_inserted),
            ):
                if not isinstance(v, str):
                    if v is None:
                        value_to_be_inserted[i] = "None"
                        continue
                    else:
                        value_to_be_inserted[i] = str(v)
                        value_to_be_inserted[i] = \
                            value_to_be_inserted[i].replace('"', "'")
                else:
                    value_to_be_inserted[i] = v
                    value_to_be_inserted[i] = \
                        value_to_be_inserted[i].replace(
                            '"',
                            "'",
                        )

                if value_to_be_inserted[i] is not None:
                    if k != "sentiment" and k != "created_utc":
                        tmp = value_to_be_inserted[i]
                        value_to_be_inserted[i] = '"' + tmp + '"'
                new_val.append(value_to_be_inserted[i])
                new_col.append(columns_to_be_inserted[i])

            return new_val, new_col

        (
            value_to_be_inserted,
            columns_to_be_inserted,
        ) = _convert_value_to_correct_type()

        columns_to_be_inserted = ",".join(columns_to_be_inserted)
        value_to_be_inserted = ",".join(value_to_be_inserted)

        return f"""INSERT INTO reddit ({columns_to_be_inserted})
        VALUES({value_to_be_inserted});
        """

    def get_table_schema_from_reddit_stream(self) -> List[str]:
        # conn = self._create_connection(sqlite_file)
        conn = self._create_connection(self.db_config)

        query = "PRAGMA table_info('reddit_stream')"
        query = "DESCRIBE reddit_stream"
        c = conn.cursor()
        c.execute(query)
        table_scheama_tuple = c.execute(query).fetchall()
        table_schema_name_list: List[str] = \
            [i[1] for i in table_scheama_tuple]

        conn.commit()
        conn.close()
        return table_schema_name_list

    def insert_processed_data_to_reddit_database(self):
        # conn = self._create_connection(sqlite_file)
        conn = self._create_connection(**self.db_config)

        column_value_dict: List[
            Union[str, List[Dict[str, Any]]]
        ] = self.all_aspect_data_dict

        for i in column_value_dict:
            query = self._reddit_insert_query(**i)
            c = conn.cursor()
            try:
                c.execute(query)
            except Exception as e:
                print(e)
                pass
            # table_scheama = c.execute(
            #     "PRAGMA table_info('reddit')").fetchall()

        conn.commit()
        conn.close()

        pass


if __name__ == "__main__":
    #=====================
    #== create or update table
    #=====================

    # BUG: I believe the following bugs are due to the fact that i have
    #  reddit_stream_data and reddit_data in the same folders.
    #  |
    #   when run SocialMetaDAtabase(..,.., update_stream_data=True)
    #     Error: table reddit_stream has no clolumns named title
    #   when run SocialMetaDAtabase(..,.., update_stream_data=False)
    #     Error: error 'o_such_column: nan'
    all_data_path = get_all_file_path()
    all_files = get_all_file(all_data_path, "reddit")
    all_data = get_all_data_from_files(all_files, "reddit")
    # SocialMediaDatabase(REDDIT_DATABASE, all_data)
    SocialMediaDatabase(REDDIT_DATABASE, all_data, False)

    #=====================
    #==convert from reddit_stream to reddit
    #=====================
    # db_type = DATABASE_TYPE[0]
    db_type = DATABASE_TYPE[1]

    if db_type == DATABASE_TYPE[0]:
        db_config = {"db_file": REDDIT_DATABASE}
        reddit_stream_class = RedditStream(db_config, db_type)
    elif db_type == DATABASE_TYPE[1]:
        db_config = {'host': MYSQL_HOST,
                     'port': MYSQL_PORT,
                     'user': MYSQL_USERNAME,
                     'password': MYSQL_PASSWORD,
                     }
        reddit_stream_class = RedditStream(db_config, db_type)
    else:
        raise ValueError

    # all_data_path = get_all_file_path()
    # all_files = get_all_file(all_data_path, "twitter")
    # all_data = get_all_data_from_files(all_files, "twitter")
    # SocialMediaDatabase(TWITTER_DATABASE, all_data)

    PROGRAM_LOGGER.info("complete running..")
