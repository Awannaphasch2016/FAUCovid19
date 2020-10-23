# -*- coding: utf-8 -*-

"""Run social media data api so users can requests for social media data."""

import datetime
import sqlite3
from itertools import product
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from typing import cast

from flask import Flask
from flask import request
from flask_restful import Api  # type: ignore

from global_parameters import ALL_ASPECTS
# Create an instance of Flask
# from global_parameters import BASE_DIR
from global_parameters import ALL_CRAWLERS
from global_parameters import ALL_FREQUENCY
from global_parameters import ALL_REDDIT_FEILDS
from global_parameters import ALL_REDDIT_SEARCH_TYPES
from global_parameters import ALL_TWITTER_FEILDS
from global_parameters import ALL_TWITTER_SEARCH_TYPES
from global_parameters import REDDIT_DATABASE
from global_parameters import TWITTER_DATABASE
from src.Utilities import MyLogger
from src.Utilities.Errors.http_errors import https_400_bad_request_template
from src.Utilities.utilities import return_error_template

LOGGER = MyLogger()
PROGRAM_LOGGER = LOGGER.program_logger

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
# app.config["DB_HOST"] = 'localhost'

# Create the API
api = Api(app)

# /?crawlers=twitter&since=2020-08-07&until=2020-08-08&aspects=work_from_home,reopen
DATEFORMAT = "%Y-%m-%d"

ALL_CRAWLERS_SEARCH_TYPE = {
    ALL_CRAWLERS[0]: ALL_TWITTER_SEARCH_TYPES,
    ALL_CRAWLERS[1]: ALL_REDDIT_SEARCH_TYPES,
}

all_crawler_fields = {
    ALL_CRAWLERS[0]: ALL_TWITTER_FEILDS,
    ALL_CRAWLERS[1]: ALL_REDDIT_FEILDS,
}


def is_reddit_fields(s):
    """
    Return true if arg is an accepted reddit's fields.

    :type s: str
    :param s: any accepted fields

    :rtype: boolean
    :return: return true if arg is an accpeted reddit fields otherwise false
    """
    return s in ALL_REDDIT_FEILDS or s == "all"


def is_twitter_fields(s):
    """
    Return true if arg is an accepted twitter's fields.

    :type s: str
    :param s: any accepted fields

    :rtype: boolean
    :return: return true if arg is an accpeted twitter fields otherwise false
    """
    return s in ALL_TWITTER_FEILDS or s == "all"


class APIManager:
    """Skipped."""

    def __init__(
            self,
            aspects,
            crawlers,
            after_date,
            before_date,
            frequency,
            search_types,
            fields,
            total_count,
            top_amount,
            page,
            limit
    ):
        """Skipped."""
        self.init_vars(
            aspects,
            crawlers,
            after_date,
            before_date,
            frequency,
            search_types,
            fields,
            total_count,
            top_amount,
            page,
            limit
        )

    def init_vars(
            self,
            aspects,
            crawlers,
            after_date,
            before_date,
            frequency,
            search_types,
            fields,
            total_count,
            top_amount,
            page,
            limit,
    ):
        """
        Prepare common data that will be used among class's methods.

        :type aspects: List of str
        :param aspects: list of aspects

        :type crawlers: List of str
        :param crawlers: list of aspects

        :type after_date: datetime.datetime
        :param after_date: date in which all aata AFTER this date should be
         retrieved

        :type before_date: datetime.datetime
        :param before_date: date in which all aata BEFORE this date should be
         retrieved

        :type frequency: Frequency
        :param frequency: interval of time to retrieved data

        :type search_types: list of str
        :param search_types: list of desired search type by crawler

        :type fields: list of str
        :param fields: list of desired fields by crawler

        :type total_count: bool
        :param total_count: it indicates whether or not to return
            total  count of the returned output instead of output itself

        :type top_amount: Optional[int]
        :param top_amount: if specified, only the most recent of the selected
            time interval range will be shown in the output

        """
        self.RETURNED_DATA_KEY = "all_retrived_data"

        self.aspects = aspects
        self.crawlers = crawlers
        self.after_date = after_date
        self.before_date = before_date
        self.frequency = frequency
        self.search_types = search_types
        self.fields = fields
        self.total_count = total_count
        self.top_retrieved_data = top_amount
        self.pages = page
        self.limit = limit

    def select_returned_function(self) -> Callable:
        """Skipped summary."""
        if self.total_count:
            return self._get_total_count
        elif self.top_retrieved_data:
            return self._get_top_retrieved_data
        elif self.pages[0] is not None:
            if self.pages[0] == 'all' and self.limit == 'inf':
                return self._get_all_retrieved_data
            return self._get_all_pages
        else:
            return self._get_all_retrieved_data

    def _get_all_pages(self):
        """Return specified pages where each len(pages) == limit."""


        total_retrived_data = \
            self._get_all_retrieved_data()[self.RETURNED_DATA_KEY]

        total_num_data = \
            list(
                range(len(total_retrived_data))
            )

        def _apply_pagination():
            all_pages = \
                [
                    total_retrived_data[i:j] for i, j in
                    zip(
                        total_num_data[::self.limit][:-1],
                        total_num_data[::self.limit][1:],
                    )
                ]
            all_pages.append(
                total_retrived_data[total_num_data[::self.limit][-1]:]
            )
            return all_pages

        all_pages = _apply_pagination()

        def _return_selected_pages():
            if self.pages[0] == 'all':
                return {
                    "select_pages": f"{self.pages[0]}",
                    self.RETURNED_DATA_KEY: all_pages
                }
            else:
                selected_pages = ','.join([str(i) for i in self.pages])
                return {
                    "select_pages": f"{selected_pages}",
                    self.RETURNED_DATA_KEY: [all_pages[i] for i in self.pages]
                }

        return _return_selected_pages()

    def _get_total_count(self) -> Dict:
        """Skipped summary."""
        return {
            "total_count": len(
                self._get_all_retrieved_data()[self.RETURNED_DATA_KEY],
            ),
        }

    def _get_top_retrieved_data(self) -> Dict:
        """Skipped summary."""
        return {
            "top_retrieved": self.top_retrieved_data,
            self.RETURNED_DATA_KEY: self._get_all_retrieved_data()[
                                        self.RETURNED_DATA_KEY
                                    ][: self.top_retrieved_data],
        }

    def _get_all_retrieved_data(self) -> Dict:
        """Skipped summary.

        Prepared + return all  stored crawled data of selected crawlers to
         browser.

         :rtype: Dict
         :return: returned all stored cralwed data of selected crawlers

        """
        returned_data: Dict[str, List[Dict]] = {}

        def _get_query(crawler, all_crawler_search_type, all_crawler_fields):
            after_date_query = ""
            before_date_query = ""

            if self.after_date[0] is None and self.before_date[0] is None:
                after_date_query = ""
                before_date_query = ""
            else:
                if crawler == "reddit":
                    date_key = " created_utc"
                elif crawler == "twitter":
                    date_key = " date "
                else:
                    raise ValueError()

                if self.after_date[0] is not None:
                    after_date_created_utc = int(
                        self.after_date[0].timestamp(),
                    )
                    after_date_query = f"{date_key} > {after_date_created_utc}"
                if self.before_date[0] is not None:
                    before_date_created_utc = int(
                        self.before_date[0].timestamp(),
                    )
                    before_date_query = (
                        f"{date_key} <= {before_date_created_utc}"
                    )

            if self.search_types[0] == "all":
                search_types = all_crawler_search_type
            else:
                search_types = self.search_types

            if self.fields[0] == "all":
                fields_query = " * "
            else:
                fields_query = ",".join(self.fields)

            aspect_query = f" aspect = '{asp}'"

            if len(search_types) == len(all_crawler_search_type):
                all_query = [aspect_query]
            else:
                tmp = []
                for t in search_types:
                    tmp.append(f" search_type = '{t}' ")
                tmp = " or ".join(tmp)
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
            else:
                frequency_query = ""

            return (
                    f"select {fields_query} from {crawler} where "
                    + " and ".join(all_query)
            )

        social_media_database_name_path = {
            ALL_CRAWLERS[1]: REDDIT_DATABASE,
            ALL_CRAWLERS[0]: TWITTER_DATABASE,
        }

        def _get_all_retrived_data(_asp: str, _crawler: str) -> List[Dict]:
            """Skipped summary.

            :type _asp:  str
            :param _asp: an aspect name

            :type _crawler:  str
            :param _crawler: a crawler name
            """
            path_to_crawler_database = social_media_database_name_path[
                _crawler
            ]

            query = _get_query(
                _crawler,
                ALL_CRAWLERS_SEARCH_TYPE[_crawler],
                all_crawler_fields[_crawler],
            )
            all_crawler_data_from_database = self._get_all_data_from_sqlite(
                _crawler,
                path_to_crawler_database,
                query,
            )

            return all_crawler_data_from_database

        for asp, crawler in product(self.aspects, self.crawlers):
            all_reddit_data: List[Dict] = _get_all_retrived_data(asp, crawler)

            returned_data.setdefault(self.RETURNED_DATA_KEY, []).extend(
                all_reddit_data,
            )

        return returned_data

    def _get_all_data_from_sqlite(
            self,
            crawler: str,
            path_to_database: str,
            query: str,
    ) -> List[Dict]:
        """Skipped summary.

        Get all stored crawled data of a specified crawler from sqlite database.

        :type  crawler:
        :param crawler:

        :type path_to_database: str
        :param path_to_database: path to dataabase


        :type query: str
        :param query: str of  character to pull data from  database

        :rtype:  list of dict
        :return:  list of dict containing all specified parameters
        """
        assert (
                crawler == path_to_database.split("\\")[-1].split("_")[0]
        ), path_to_database

        # print(path_to_database)
        conn = sqlite3.connect(path_to_database)
        cur = conn.cursor()
        cur.execute(query)

        def unroll_all_variable_in_fields():
            if self.fields[0] == "all" and crawler == "reddit":
                return ALL_REDDIT_FEILDS
            if self.fields[0] == "all" and crawler == "twitter":
                return ALL_TWITTER_FEILDS
            return self.fields

        fields = unroll_all_variable_in_fields()

        if "crawler" in fields:
            r = [
                {
                    **{
                        cur.description[i][0]: value
                        for i, value in enumerate(row)
                    },
                    **{"crawler": crawler},
                }
                for row in cur.fetchall()
            ]
        else:
            r = [
                {
                    **{
                        cur.description[i][0]: value
                        for i, value in enumerate(row)
                    },
                }
                for row in cur.fetchall()
            ]
        # self.conn.commit()
        conn.close()
        return r

    def _get_retrieved_data_from_a_file(self, all_data_from_a_file):
        """Skipped summary."""
        pass


def is_date(date_string):
    """Skipped summary.

    Return true if parameter is a date with a specified format (%Y-%m-%d)
    otherwise false.

    :type date_string: str
    :param date_strng: date in the following format %Y-%m-%d

    :rtype: boolean
    :return: return true if arg is an accpeted frequency otherwise flase
    """
    try:
        return True
    except ValueError as e:
        PROGRAM_LOGGER.error(
            "This is the incorrect date string format. It should be %Y-%m-%d "
            "for example 12-25-2018",
        )
        raise ValueError(e)


def is_supported_frequency(freq):
    """
    Return true if arg is an accpeted frequency otherwise false.

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
    Return true if arg is an accpeted frequency.

    :type asp: str
    :param asp: any accpeted frequency str

    :rtype: boolean
    :return: return true if arg is an accpeted frequency
    """
    return asp in ALL_ASPECTS or asp is None


def is_supported_crawler(cr):
    """
    Return true if arg is an supported crawler.

    :type cr: str
    :param cr: any accpeted crawler str

    :rtype: boolean
    :return: return true if arg is an accpeted crawler
    """
    return cr in ALL_CRAWLERS or cr is None


# def is_search_types(cr):
#     return cr in ALL_SEARCH_TYPES


def get_respond_type_when_crawler_is_all(cr):
    """Skipped summary.

    return list of crawler's respond type when arg == 'all' else output arg
    without change

    :param cr: str
    :param cr: any accepted crawler

    :return: list of str
    :return: list of crawler name
    """
    if cr == "reddit":
        search_types = ALL_REDDIT_SEARCH_TYPES
    if cr == "twitter":
        search_types = search_types, ALL_TWITTER_SEARCH_TYPES

    return search_types


@app.route("/", methods=["GET"])
def index():
    """Skipped summary.

    prepared specified input parameters and return all retirieved data in
    database in json format

    :rtype:  json
    :return: all retrieved data in database
    """
    crawlers = request.args.get("crawlers")
    since = request.args.get("since")
    until = request.args.get("until")
    # after =  request.args.get('after')
    aspects = request.args.get("aspects")
    search_types = request.args.get("search_types")
    frequency = request.args.get("frequency")
    fields = request.args.get("fields")
    total_count = request.args.get("total_count")
    top_amount = request.args.get("top_amount")
    limit = request.args.get("limit")
    pages = request.args.get("pages")

    def _check_compatibility_of_top_amount_and_total_count(
            _top_amount: Optional[str],
            _total_count: Optional[str],
            _page: Optional[str],
            _limit: Optional[str]
    ) -> \
            Optional[
                Tuple[str, int]
            ]:
        count = 0
        if _top_amount is not None:
            count += 1
        if _total_count is not None:
            count += 1
        if _page is not None:
            if _limit is None:
                return https_400_bad_request_template(
                    "Either top_amount,total_count, or pages&limit must be "
                    "provided. Not Both.",
                )
            count += 1
        if count >= 2:
            return https_400_bad_request_template(
                "Either top_amount,total_count, or pages&limit must be "
                "provided. Not Both.",
            )
        return None

    def _check_compatibility_of_page_limit(
            _page: Optional[str], _limit: Optional[str],
    ) -> \
            Optional[
                Tuple[str, int]
            ]:
        if _page is not None and _limit is None:
            return https_400_bad_request_template(
                "More explicit is required: when page is specified, "
                "limit must also be specified.",
            )
        return None

    def _check_param_compatibility(
            _check_param_compatibility_func,
            *args
    ) -> Optional[Tuple[str, int]]:
        """Skipped summary.

        :type _total_count: bool
        :param _total_count: it indicates whether or not to return
            total  count of the returned output instead of output itself

        :type _top_amount: Optional[int]
        :param _top_amount: if specified, only the most recent of the selected
            time interval range will be shown in the output

        :rtype: Tuple[str,int]
        :return: tuple of error message and error status code
        """

        params_error = _check_param_compatibility_func(*args)
        return params_error

    params_error = \
        _check_param_compatibility(
            _check_compatibility_of_top_amount_and_total_count
            , top_amount, total_count, pages, limit
        )

    if params_error is not None:
        return params_error

    params_error = \
        _check_param_compatibility(
            _check_compatibility_of_page_limit
            , pages, limit
        )

    if params_error is not None:
        return params_error

    def _convert_none_value_to_appropriate_value(
            _crawlers: Optional[Union[str, List[str]]],
            _since: Any,
            _until: Any,
            _aspects: Optional[Union[str, List[str]]],
            _search_types: Any,
            _fields: Optional[Union[str, List[str]]],
            _frequency: Optional[Union[str, List[str]]],
            _total_count: Optional[bool],
            _top_amount: Optional[str],
            _page: Optional[str],
            _limit: Optional[str],
    ) -> Tuple[Union[List, str],
               Optional[str],
               Optional[str],
               Union[str, List[str]],
               Any,
               Optional[Union[str, List[str]]],
               Union[str, List[str]],
               bool,
               Optional[int],
               str,
               Union[str,int]]:
    # ) -> Any:
        if _aspects is None:
            _aspects = "all"

        if _frequency is None:
            _frequency = "day"

        if _crawlers is None:
            _crawlers = "all"

        if _total_count is None or _total_count == "false":
            _total_count = False
        else:
            if _total_count == "true":
                _total_count = True
            else:
                raise ValueError()

        _top_amount_: Optional[int]
        if _top_amount is not None:
            if isinstance(_top_amount, str):
                _top_amount_ = int(_top_amount)
            else:
                raise ValueError()
        else:
            _top_amount_ = None

        if _page is not None:
            if isinstance(_page, str):
                _page = _page
            else:
                raise ValueError()
        else:
            _page = 'all'

        _limit_: Union[int,str]
        if _limit is not None:
            if isinstance(_limit, str):
                _limit_ = int(_limit)
            else:
                raise ValueError()
        else:
            _limit_ = 'inf'

        # Tuple[Union[List, str], Optional[str], Optional[str],
        # str, str, str, str, bool, int, int, str]:

        return (
            _crawlers,
            _since,
            _until,
            _aspects,
            _search_types,
            _fields,
            _frequency,
            _total_count,
            _top_amount_,
            _page,
            _limit_,
        )
        # return (
        #     _crawlers,
        #     _since,
        #     _until,
        #     _aspects,
        #     _search_types,
        #     _fields,
        #     _frequency,
        #     _total_count,
        #     _top_amount_,
        #     _limit_,
        #     _page,
        # )

    (
        crawlers,
        since,
        until,
        aspects,
        search_types,
        fields,
        frequency,
        total_count,
        top_amount,
        pages,
        limit,
    ) = _convert_none_value_to_appropriate_value(crawlers,
                                                 since,
                                                 until,
                                                 aspects,
                                                 search_types,
                                                 fields,
                                                 frequency,
                                                 total_count,
                                                 top_amount,
                                                 pages,
                                                 limit,
                                                 )

    def _is_reddit_search_type(s):
        return s in ALL_REDDIT_SEARCH_TYPES or s == "all"

    def _is_twitter_search_type(s):
        return s in ALL_TWITTER_SEARCH_TYPES or s == "all"

    def _ensure_compatiblity_of_search_types_and_crawlers(c, st, f):
        ENSURE_KEY: List[str] = ["search_types", "fields_types"]
        REDDIT_ENSURE_FUNCTION: Dict = {
            ENSURE_KEY[0]: _is_reddit_search_type,
            ENSURE_KEY[1]: is_reddit_fields,
        }
        TWITTER_ENSURE_FUNCTION: Dict = {
            ENSURE_KEY[0]: _is_twitter_search_type,
            ENSURE_KEY[1]: is_twitter_fields,
        }
        ALL_CRALWER_ENSURE_FUNCTION: Dict = {
            ALL_CRAWLERS[0]: TWITTER_ENSURE_FUNCTION,
            ALL_CRAWLERS[1]: REDDIT_ENSURE_FUNCTION,
        }

        def _get_ensure_compatibility_dict(
                _crawler: str,
                ensure_function_type: str,
        ):
            return ALL_CRALWER_ENSURE_FUNCTION[_crawler][ensure_function_type]

        if st is None:
            st = "all"
        if f is None:
            f = "all"

        search_types_split = st.split(",")
        fields_split = f.split(",")

        args_split = {
            ENSURE_KEY[0]: search_types_split,
            ENSURE_KEY[1]: fields_split,
        }

        if c in ALL_CRAWLERS:
            for i in args_split[ENSURE_KEY[0]]:
                assert _get_ensure_compatibility_dict(c, ENSURE_KEY[0])(i)
            for i in args_split[ENSURE_KEY[1]]:
                assert _get_ensure_compatibility_dict(c, ENSURE_KEY[1])(i)
            return [c], search_types_split, fields_split
        else:
            crawler_split = c.split(",")
            if len(crawler_split) == len(ALL_CRAWLERS):
                for i in crawler_split:
                    assert is_supported_crawler(i)

                return ["all"], ["all"], ["all"]
            else:
                raise ValueError

    def _applying_all_value_condition(
            _crawlers: Optional[Union[str, List[str]]],
            _search_types: Optional[Union[str, List[str]]],
            _fields: Optional[Union[str, List[str]]],
    ) -> Union[List[Union[str, List[str],None]], Tuple[str, int]]:

        if _crawlers != "all" and _crawlers is not None:
            (
                _crawlers,
                _search_types,
                _fields,
            ) = _ensure_compatiblity_of_search_types_and_crawlers(
                _crawlers,
                _search_types,
                _fields,
            )
        elif _crawlers == "all":
            if _fields is not None:
                return https_400_bad_request_template(
                    "Do you forget to specified crawler_type? "
                    "fields must always be specified with specific cralwer"
                )
            if _search_types is not None:
                return https_400_bad_request_template(
                    "Do you forget to specified crawler_type? "
                    "search_types must always be specified with specific "
                    "cralwer"
                )
            _search_types = ["all"]
            _fields = ["all"]
        else:
            raise ValueError
        return [_crawlers, _search_types, _fields]

    has_error = _applying_all_value_condition(
        crawlers, search_types, fields,
    )

    if return_error_template(has_error) is not None:
        return has_error
    crawler, search_types, fields = has_error

    def convert_to_common_type(args, all_keywords=None, accept_all=True):
        if accept_all:
            assert all_keywords is not None, ""
        else:
            assert all_keywords is None, ""

        if args is None:
            return [None]
        if accept_all:
            args = args if isinstance(args, list) else args.split(",")
            if len(args) == 1 and args[0] == "all":
                return all_keywords
            else:
                return args
        else:
            try:
                return [int(i) for i in args.split(",")]
            except:
                return args.split(",")

    crawlers = convert_to_common_type(crawlers, ALL_CRAWLERS)
    aspects = convert_to_common_type(aspects, ALL_ASPECTS)
    since = convert_to_common_type(since, accept_all=False)
    until = convert_to_common_type(until, accept_all=False)
    frequency = convert_to_common_type(frequency, accept_all=False)
    pages = convert_to_common_type(pages, accept_all=False)

    def _check_param_types(
            _crawlers: Optional[Union[str, List[str]]],
            _since: List[Optional[str]],
            _until: List[Optional[str]],
            _aspects: List[str],
            _search_types: Any,
            _frequency: List[str],
            _total_count: bool,
            _top_amount: int,
            _page: str,
            _limit: str,
    ) -> Union[
        Tuple[List[datetime.datetime], List[datetime.datetime]],
        Tuple[str, int]
    ]:

        for aspect in _aspects:
            assert is_supported_aspect(aspect)

        if _since[0] is not None:
            # assert is_date(_since[0]) and len(_since) == 1
            try:
                since_datetime = [
                    datetime.datetime.strptime(_since[0], DATEFORMAT),
                ]
            except:
                return https_400_bad_request_template(
                    "since params only except dateformat = %Y-%m-%d"
                )
        else:
            since_datetime = _since

        _until =  cast(List[str], _until)
        if _until[0] is not None or _until[0] == "all":
            # assert is_date(_until[0]) and len(_until) == 1

            try:
                until_datetime = [
                    datetime.datetime.strptime(_until[0], DATEFORMAT),
                ]
            except:
                return https_400_bad_request_template(
                    "until params only except dateformat = %Y-%m-%d"
                )
        else:
            until_datetime = _until

        assert is_supported_frequency(_frequency[0])

        if _top_amount is not None:
            assert isinstance(_top_amount, int), ""

        if _top_amount is not None:
            assert isinstance(_top_amount, int), ""

        if _page is not None and _page[0] != 'all':
            for i in _page:
                assert isinstance(i, int), ""

        if _limit is not None and _limit != 'inf':
            assert isinstance(_limit, int), ""

        assert isinstance(_total_count, bool), ""

        return since_datetime, until_datetime

    has_error = _check_param_types(
        crawlers,
        since,
        until,
        aspects,
        search_types,
        frequency,
        total_count,
        top_amount,
        pages,
        limit
    )

    if return_error_template(has_error) is not None:
        return has_error

    since_datetime, until_datetime = has_error

    api_manager = APIManager(
        aspects,
        crawlers,
        since_datetime,
        until_datetime,
        frequency,
        search_types,
        fields,
        total_count,
        top_amount,
        pages,
        limit
    )

    return api_manager.select_returned_function()()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(host='127.0.0.1', port=5501, debug=True)
