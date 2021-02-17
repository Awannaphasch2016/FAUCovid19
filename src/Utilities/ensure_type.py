# -*- coding: utf-8 -*-

"""Contain common functions that ensure type to be passed."""

import datetime
from typing import Optional
from typing import Tuple
from typing import Union

from typing_extensions import NoReturn

from src.Utilities import Frequency
from src.Utilities import MyLogger
from src.Utilities.time_utility import (
    _convert_timedelta_to_specified_frequency,
)

LOGGER = MyLogger()
PROGRAM_LOGGER = LOGGER.program_logger
DEBUG_LOGGER = LOGGER.debug_logger



def only_download_full_day(
        frequency: str,
        before: Optional[int],
        after: int,
# ) -> Union[NoReturn, None]:
) -> None:
    """Ensure that full day of data can be collected before download.

    :type frequency:
    :param frequency:

    :type before:
    :param before:

    :type after:
    :param after:

    :rtype:
    :return:
    """
    if frequency == "day":

        def is_full_day(before: Optional[int], after: int) -> bool:
            """Exclude data from today aka datetime.datetime.now().day ."""
            if before == 0:
                PROGRAM_LOGGER.info(
                    "!!! exclude data from today aka "
                    "datetime.datetime.now().day => to make sure that only "
                    "full day of data will be loaded !!!",
                )
                return False
            else:
                return True

        if not is_full_day(before, after):
            return

    else:
        raise NotImplementedError


def ensure_epoch_datetime(date: datetime.datetime) -> int:
    """Ensure that date contain epoch datetime."""
    epoch_datetime = str(date.timestamp()).split(".")[0]
    assert len(epoch_datetime) == 10, ""
    return int(epoch_datetime)


def _ensure_datetime_for_specified_frequency_not_consider_max_after(
    after_timestamp_utc: datetime.datetime,
    max_after: datetime.datetime,
    frequency: Frequency,
    after: int,
) -> int:
    """Ensure that datetime for specified frequency."""
    time_diff = max_after - after_timestamp_utc

    after_in_specified_frequency = _convert_timedelta_to_specified_frequency(
        time_diff,
        frequency,
    )

    # if after_timestamp_utc.date() < max_after_timestamp_utc.date():
    #     # FIXME:
    #     #  :logic here does not make sense ( what does it expected to od
    #     #  from places that it is called from
    #     #  :relation between after and after_timestamp_utc (when it does
    #     #  and does not exceed max)
    #     after_timestamp_utc = _get_epoch_datetime_subtract_timedelta(
    #         datetime.datetime.now(), frequency, after)
    #
    #     time_diff = max_after_timestamp_utc - after_timestamp_utc
    #
    #     after_in_specified_frequency = \
    #         _convert_timedelta_to_specified_frequency(time_diff, frequency)
    #     after = after_in_specified_frequency
    #
    #     after_timestamp_utc = max_after_timestamp_utc

    return after_in_specified_frequency
    # return  after_timestamp_utc,  after


if __name__ == "__main__":
    _ensure_datetime_for_specified_frequency_not_consider_max_after(
        datetime.datetime.now(),
        datetime.datetime.now(),
        "day",
        20,
    )
