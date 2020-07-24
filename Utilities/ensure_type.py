import datetime
import json
from typing import Dict
from typing import Tuple

from Utilities.declared_typing import Frequency
from Utilities.declared_typing import Json
from Utilities.time_utility import _convert_timedelta_to_specified_frequency
from Utilities.time_utility import _get_epoch_datetime_subtract_timedelta


def ensure_epoch_datetime(date: datetime.datetime) -> int:
    epoch_datetime = str(date.timestamp()).split('.')[0]
    assert len(epoch_datetime) == 10, ''
    return int(epoch_datetime)


# def _ensure_datetime_for_specified_frequency_not_consider_max_after(after_timestamp_utc: datetime.datetime,
#                                                                     max_after:datetime.datetime,
#                                                                     frequency: Frequency,
#                                                                     after: int) -> int:
#
#     time_diff = max_after - after_timestamp_utc
#
#     after_in_specified_frequency = _convert_timedelta_to_specified_frequency(
#         time_diff, frequency)
#
#     # if after_timestamp_utc.date() < max_after_timestamp_utc.date():
#     #     # HERE
#     #     #  :logic here does not make sense ( what does it expected to od from places that it is called from
#     #     #  :relation between after and after_timestamp_utc (when it does and does not exceed max)
#     #     after_timestamp_utc = _get_epoch_datetime_subtract_timedelta(
#     #         datetime.datetime.now(), frequency, after)
#     #
#     #     time_diff = max_after_timestamp_utc - after_timestamp_utc
#     #
#     #     after_in_specified_frequency = _convert_timedelta_to_specified_frequency(
#     #         time_diff, frequency)
#     #     after = after_in_specified_frequency
#     #
#     #     after_timestamp_utc = max_after_timestamp_utc
#
#     return after_in_specified_frequency
#     # return  after_timestamp_utc,  after
