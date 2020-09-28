#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains time utility function."""

import datetime
from typing import Dict


def _get_epoch_datetime_subtract_timedelta(
    timestamp: datetime.datetime,
    frequency: str,
    interval: int,
) -> datetime.datetime:
    """Get epoch datetime - interval time."""
    if frequency == "day":
        after_timestamp_utc = timestamp - datetime.timedelta(days=interval)
    elif frequency == "hour":
        after_timestamp_utc = timestamp - datetime.timedelta(hours=interval)
    elif frequency == "minute":
        after_timestamp_utc = timestamp - datetime.timedelta(minutes=interval)
    elif frequency == "second":
        after_timestamp_utc = timestamp - datetime.timedelta(seconds=interval)
    else:
        raise NotImplementedError
    return after_timestamp_utc


def _convert_timedelta_to_specified_frequency(
    duration: datetime.timedelta,
    frequency: str,
) -> int:
    """Convert timedelta to specified freqeyncy."""
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if frequency == "day":
        return days
    elif frequency == "hour":
        return hours
    elif frequency == "minute":
        return minutes
    elif frequency == "second":
        return seconds
    else:
        raise NotImplementedError

def group_respond_data_per_day(respond_data: Dict, date: datetime.datetime):
    pass

if __name__ == "__main__":
    date = 1601195531
    group_respond_data_per_day(5, date)
    pass