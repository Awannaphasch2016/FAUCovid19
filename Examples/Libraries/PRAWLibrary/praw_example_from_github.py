import inspect
import sqlite3
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import praw

# from TwitterStreamWithAWS.credentials import REDDIT_CLIENT_ID
# from TwitterStreamWithAWS.credentials import REDDIT_CLIENT_SECRET
# from TwitterStreamWithAWS.credentials import REDDIT_PASSWORD
# from TwitterStreamWithAWS.credentials import REDDIT_USERNAME
from TwitterStreamWithAWS.credentials import REDDIT_USER_AGENT

from TwitterStreamWithAWS.global_params import (
    ALL_SUBREDDIT_REPRESETED_COUNTRY_SUBREDDIT,
)
from TwitterStreamWithAWS.global_params import (
    ALL_SUBREDDIT_REPRESETED_GENERAL_COVID_SUBREDDIT,
)
from TwitterStreamWithAWS.global_params import (
    ALL_SUBREDDIT_REPRESETED_REGION_COVID_SUBREDDIT,
)
from TwitterStreamWithAWS.global_params import (
    ALL_SUBREDDIT_REPRESETED_STATES_COVID_SUBREDDIT,
)
from TwitterStreamWithAWS.global_params import REDDIT_DATABASE
from TwitterStreamWithAWS.global_params import STREAM_COMMENTS_DATA_KEYS
from TwitterStreamWithAWS.src.Services.RedditTwitterDataAPI.reddit_twitter_data_api_with_sqlite.update_sqlite3_database import (
    SocialMediaDatabase,
)
from TwitterStreamWithAWS.src.Utilities import MyLogger

LOGGER = MyLogger()
PROGRAM_LOGGER = LOGGER.program_logger

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    password=REDDIT_PASSWORD,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
)
# =====================
# == name of subreddits
# =====================
General = ALL_SUBREDDIT_REPRESETED_GENERAL_COVID_SUBREDDIT
Country = ALL_SUBREDDIT_REPRESETED_COUNTRY_SUBREDDIT
Region = ALL_SUBREDDIT_REPRESETED_REGION_COVID_SUBREDDIT
states_subreddit = ALL_SUBREDDIT_REPRESETED_STATES_COVID_SUBREDDIT

General_str = "+".join(General)
Country_str = "+".join(Country)
Region_str = "+".join(Region)
states_subreddit_str = "+".join(states_subreddit)

all_searched_subreddits = "+".join(
    [General_str, Country_str, Region_str, states_subreddit_str]
)
all_subreddit_submission_are_collected_from = {}


def get_all_class_attributes(my_class: Callable) -> List[str]:
    all_attributes = inspect.getmembers(
        my_class, lambda a: not (inspect.isroutine(a)))
    public_atributes = [
        a
        for a in all_attributes
        if not ((a[0].startswith("__") and a[0].endswith("__")))
    ]
    return public_atributes


# for comment in reddit.subreddit("all").stream.comments():
for comment in reddit.subreddit(all_searched_subreddits).stream.comments():

    subreddit: str = comment.subreddit

    all_comment_attributes: Dict = dict(get_all_class_attributes(comment))

    columns_and_value_tuple_dict: Dict[str, Any] = {
        i: j
        for i, j in all_comment_attributes.items()
        if i in STREAM_COMMENTS_DATA_KEYS
    }

    def _convert_type_to_sqlite_type() -> Dict:
        tmp: Dict = {}
        for i, j in columns_and_value_tuple_dict.items():

            if isinstance(j, (float, bool, int, str)):
                pass
            else:
                # NOTE: I don't know how to check that var is of type class
                #   without knowning the class name
                tmp[i] = str(j)

        for i, j in tmp.items():
            columns_and_value_tuple_dict[i] = j

        return columns_and_value_tuple_dict

    columns_and_value_tuple_dict = _convert_type_to_sqlite_type()

    input_data_to_SocialMediaDatabase: Dict[str, List[Dict[str, Any]]] = {
        "reddit": [columns_and_value_tuple_dict]
    }

    try:
        social_media_database = SocialMediaDatabase(
            REDDIT_DATABASE, input_data_to_SocialMediaDatabase, update_stream_data=True
        )
    except sqlite3.IntegrityError as e:

        PROGRAM_LOGGER.error(f"Error occurs:`{e}`")
        # raise Exception(e)

    except Exception as e:
        PROGRAM_LOGGER.error(f"Error occurs:`{e}`")
        raise Exception(e)
