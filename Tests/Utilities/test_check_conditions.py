from typing import Literal

import pytest

from global_parameters import ALL_ASPECTS
from global_parameters import ALL_REDDIT_TAGS
from src.Utilities.CheckConditions.check_conditions import \
    check_crawler_tags_value
from src.Utilities.CheckConditions.check_conditions import \
    check_that_all_selected_fields_are_returns
from src.Utilities.CheckConditions.check_conditions import check_response_keys
from src.Utilities.CheckConditions.check_conditions import \
    check_running_conditions

# ALL_ASPECTS = [
#     "work_from_home",
#     "social_distance",
#     "corona",
#     "reopen",
#     "lockdown",
# ]

class TestRedditTags:

    @pytest.mark.test_reddit_crawler_tags
    def test_check_reddit_tags_value_is_tuple(self):
        tags = ALL_ASPECTS[0]
        with pytest.raises(ValueError):
            check_crawler_tags_value(tags, ALL_REDDIT_TAGS)

        tags = [ALL_ASPECTS[0]]
        check_crawler_tags_value(tags, ALL_REDDIT_TAGS)

    @pytest.mark.test_reddit_crawler_tags
    def test_check_reddit_tags_value_accpets_all(self):
        tags = ["all"]
        check_crawler_tags_value(tags, ALL_REDDIT_TAGS)

    @pytest.mark.test_reddit_crawler_tags
    def test_check_reddit_tags_value_reject_None(self):
        tags = [None]
        with pytest.raises(ValueError):
            check_crawler_tags_value(tags, ALL_REDDIT_TAGS)

        tags = None
        with pytest.raises(ValueError):
            check_crawler_tags_value(tags, ALL_REDDIT_TAGS)

    @pytest.mark.test_reddit_crawler_tags
    def test_check_reddit_tags_value_fails_all_value_constraint(self):
        """Test when passing `all` value can fail."""
        tags = [ALL_ASPECTS[0], 'all']
        with pytest.raises(ValueError):
            check_crawler_tags_value(tags, ALL_REDDIT_TAGS)

def test_check_response_keys():
    # test that there are only 3 keys "metadata", `data`, `aggs`
    response_data = {
        'metadata': None,
        'data': None,
        'aggs': None
    }

    check_response_keys(response_data)


# def test_check_running_conditions_for_reddit():
#     MODE = Literal['r', 'rb', 'w', 'wb']
#     # TODO: figure it out a way to test all of the keys
#     # TODO: testing input is type RunningConditions
#     running_conditions = {
#         "crawler_"
#     }
#     check_running_conditions()

# def test_check_running_conditions_for_twitter():
#     # TODO: testing input is type RunningConditions
#     check_running_conditions()

# _check_that_all_selected_fields_are_returns()