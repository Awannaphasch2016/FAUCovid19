# -*- coding: utf-8 -*-

"""check code in """

from typing import List
from typing import Type
from typing import Union
# from Sources.Preparations.Data.RedditCrawler import RedditCrawler
# from Sources.Preparations.Data.TwitterCrawler import TwitterCrawler
from typing import cast

from global_parameters import ALL_CRAWLERS
from global_parameters import ALL_REDDIT_COLLECTION_NAMES
from global_parameters import ALL_REDDIT_SEARCH_TYPES
from global_parameters import ALL_REDDIT_TAGS
from global_parameters import ALL_TWITTER_COLLETION_NAMES
from global_parameters import ALL_TWITTER_SEARCH_TYPES
from global_parameters import ALL_TWITTER_TAGS
from src.Utilities import Json
from src.Utilities import RedditResponse
from src.Utilities import RedditRunningConstraints
from src.Utilities import RunningConditions
# from Utilities.declared_typing import RunningConstraints
from src.Utilities import Tags
from src.Utilities import TwitterRunningConstraints


def check_crawler_tags_value(
        tags: Tags,
        all_crawler_tags: List[str],
) -> None:
    # VALIDATE: I have to test that tags is LIST or Tuple type not Iterable
    # if isinstance(tags, Iterable):
    if isinstance(tags, list):

        if len(tags) == 1 and tags[0] == "all":
            return
        # elif len(tags) == 1 and tags[0] is None:
        elif len(tags) == 1 and tags[0] is None:  # NOTE: no longer support
            raise ValueError('No longer support tags = None.')

        for i in tags:
            if i not in all_crawler_tags or i in "all":
                all_tags = ",".join(tags)
                raise ValueError(
                    f"one of the following tags are not supported {all_tags}"
                )
        return
    else:
        raise ValueError("tags must have List[str]")


def check_response_keys(res: Union[RedditResponse, Json]):
    assert "metadata" in res, ""
    assert "data" in res, ""
    assert "aggs" in res, ""


def check_running_conditions(running_conditions: RunningConditions) -> None:
    for i in [
        "respond_type",
        "collection_name",
        "crawler_option",
        "search_type",
    ]:
        if i not in running_conditions:
            raise ValueError("")

        if running_conditions["crawler_option"] not in ALL_CRAWLERS:
            raise ValueError("crawler_option are not availble")
        else:

            # crawler_option = reddit
            if running_conditions["crawler_option"] == ALL_CRAWLERS[1]:
                if (
                        running_conditions["collection_name"]
                        not in ALL_REDDIT_COLLECTION_NAMES
                ):
                    raise ValueError("collection_name are not availble")

                if (
                        running_conditions["search_type"]
                        not in ALL_REDDIT_SEARCH_TYPES
                ):
                    raise ValueError("search_type are not abailble")

                if running_conditions["respond_type"] not in ["data"]:
                    raise ValueError("respond_type are not availble")


            # crawler_option = twitter
            elif running_conditions["crawler_option"] == ALL_CRAWLERS[0]:
                if (
                        running_conditions["collection_name"]
                        not in ALL_TWITTER_COLLETION_NAMES
                ):
                    raise ValueError("collection_name are not availble")

                if (
                        running_conditions["search_type"]
                        not in ALL_TWITTER_SEARCH_TYPES
                ):
                    raise ValueError("search_type are not abailble")

                if running_conditions["respond_type"] not in [
                    "data_geo",
                    "data_tweet",
                ]:
                    raise ValueError("respond_type are not availble")


def check_that_all_selected_fields_are_returns(
        running_constraints: Union[
            RedditRunningConstraints, TwitterRunningConstraints
        ],
        res: Json,
        ind: int,
        current_condition_str: str,
        verbose: int,
):
    # before = running_constraints['before']
    # after = running_constraints['after']
    fields = cast(str, running_constraints["fields"])

    current_condition_str_with_ind = (
            current_condition_str + f" || ind = {ind} ||"
    )
    res_data = res["data"][ind]
    len_res_data_key = len(list(res_data.keys()))
    num_fields = len(fields.split(","))

    if len_res_data_key != num_fields:

        def get_missing_keys():
            incorrect_fields = set(res_data.keys()).symmetric_difference(
                set(fields.split(","))
            )
            all_missing_keys = "[" + ",".join(list(incorrect_fields)) + "]"
            incorrect_fields_error = (
                f"{current_condition_str_with_ind} "
                f"the following fields are incorrect"
                f" {all_missing_keys} "
            )
            return (
                list(incorrect_fields),
                all_missing_keys,
                incorrect_fields_error,
            )

        def add_missing_keys(
                incorrect_fields: List,
                all_missing_keys: str,
                incorrect_fields_error: str,
        ):
            if verbose:
                print(
                    f"{current_condition_str_with_ind}  "
                    f"adding keys = {all_missing_keys}"
                )

            for missing_key in incorrect_fields:
                if missing_key not in res["data"]:
                    res["data"][ind][missing_key] = None

            assert len(list(res["data"][0])) == num_fields, get_missing_keys()[
                2
            ]

        add_missing_keys(*get_missing_keys())

    else:
        print(
            f"{current_condition_str_with_ind} || "
            f"all selected fields are retuned "
        )
