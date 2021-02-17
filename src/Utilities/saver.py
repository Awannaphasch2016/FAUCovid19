#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Container utility related to saving to file."""

import datetime
import os
import pathlib
import pickle
from typing import Any
from typing import cast


def get_full_datetime_str(timestamp: datetime.date) -> str:
    """Convert timestamp into an acceptable format.

    :type timestamp: datetime.datetime
    :param timestamp: any date

    :rtype: str
    :return: date string with replaced 'space', ':', '.' as '-'
    """
    timestamp_: str = str(timestamp).replace(" ", "-")
    timestamp_ = str(timestamp_).replace(":", "-")
    timestamp_ = str(timestamp_).replace(".", "-")

    return timestamp_


def get_saved_file_path(
    time_since: datetime.date,
    date_since: datetime.date,
    path_name: pathlib.Path,
) -> pathlib.Path:
    """Get saved file path.

    :param time_since_:
    :param date_since_:
    :param path_name:
    :return:
    """
    time_since_: str  = get_full_datetime_str(time_since)
    date_since_: str  = get_full_datetime_str(date_since)

    saved_file = (
        pathlib.Path(path_name)
        / f"after_date={time_since_}_to_{date_since_}.pickle"
    )
    return saved_file

def get_saved_file_path_for_1_full_day(
    date: datetime.date,
    path_name: pathlib.Path,
) -> pathlib.Path:
    """Get saved file path.

    :param time_since_:
    :param date_since_:
    :param path_name:
    :return:
    """
    date: str  = get_full_datetime_str(date)

    saved_file = (
        pathlib.Path(path_name)
        / f"date={date}.pickle"
    )
    return saved_file


def save_to_file(content: Any, saved_file: pathlib.Path) -> None:
    """Save content to specified path."""
    path = str(pathlib.Path(saved_file).parent)

    if not os.path.exists(path):
        os.makedirs(path)

    with open(str(saved_file.resolve()), "wb") as f:
        pickle.dump(content, f)
        print(f"saved at {f.name}")
        print()

if __name__ == '__main__':
    print('hi')