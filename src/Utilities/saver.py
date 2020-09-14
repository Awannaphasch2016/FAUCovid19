#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Container utility related to saving to file."""

import datetime
import os
import pathlib
import pickle
from typing import Any


def get_full_datetime_str(timestamp: datetime.datetime) -> str:
    """Convert timestamp into an acceptable format.

    :type timestamp: datetime.datetime
    :param timestamp: any date

    :rtype: str
    :return: date string with replaced 'space', ':', '.' as '-'
    """
    timestamp = str(timestamp).replace(" ", "-")
    timestamp = str(timestamp).replace(":", "-")
    timestamp = str(timestamp).replace(".", "-")

    return timestamp


def get_saved_file_path(
    time_since: datetime.datetime,
    date_since: datetime.datetime,
    path_name: pathlib.Path,
) -> pathlib.Path:
    """Get saved file path.

    :param time_since:
    :param date_since:
    :param path_name:
    :return:
    """
    time_since = get_full_datetime_str(time_since)
    date_since = get_full_datetime_str(date_since)

    saved_file = (
        pathlib.Path(path_name)
        / f"after_date={time_since}_to_{date_since}.pickle"
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
