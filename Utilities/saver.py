import os
import pickle
import datetime
from typing import Any
import pathlib

def get_full_datetime_str(timestamp: datetime.datetime)-> str:
    timestamp = str(timestamp).replace(' ','-')
    timestamp = str(timestamp).replace(':','-')
    timestamp = str(timestamp).replace('.','-')

    return  timestamp

def get_saved_file_path(time_since: datetime.datetime,
                        date_since: datetime.datetime,
                        path_name: pathlib.Path) -> pathlib.Path:

    time_since = get_full_datetime_str(time_since)
    date_since = get_full_datetime_str(date_since)

    saved_file = pathlib.Path(
        path_name) / f'after_date={time_since}_to_{date_since}.pickle'
    return saved_file

def save_to_file(content: Any,
                 saved_file: pathlib.Path) -> None:

    path = str(pathlib.Path(saved_file).parent)

    if not os.path.exists(path):
        os.makedirs(path)

    with open(str(saved_file.resolve()), 'wb') as f :
        pickle.dump(content, f)
        print(f'saved at {f.name}')
