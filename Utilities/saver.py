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

def get_saved_file_path(date_since: datetime.datetime,
                        date_until: datetime.datetime,
                        path_name: pathlib.Path) -> pathlib.Path:

    date_since = get_full_datetime_str(date_since)
    date_until = get_full_datetime_str(date_until)

    saved_file = pathlib.Path(
        path_name) / f'after_date={date_since}_to_{date_until}.pickle'
    return saved_file

def save_to_file(content: Any,
                 saved_file: pathlib.Path) -> None:

    path = str(pathlib.Path(saved_file).parent)

    if not os.path.exists(path):
        os.makedirs(path)

    with open(str(saved_file.resolve()), 'wb') as f :
        pickle.dump(content, f)
        print(f'saved at {f.name}')
