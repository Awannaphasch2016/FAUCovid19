
import os
import pathlib
import pickle
from os import walk

#=====================
#== get all file beginning with date (naming style for version of
# reddit crawler using psaw)
#=====================
from global_parameters import ALL_ASPECTS

mypath = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data\RedditCrawler\corona\corona_countries\comment\data'

import os
result = [ f for dp, dn, filenames in os.walk(mypath)
           for f in filenames
           if f.startswith('date')]
print(result)


#=====================
#== get files for each aspects.
#=====================

mypath = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data' \
         r'\RedditCrawler'
import os
all_aspects_files_dict = {i: [] for i in ALL_ASPECTS}
all_files = []
for dp, dn, filenames in os.walk(mypath):
    for f in filenames:
        if f.startswith('date'):
            aspect = dp.split('\\')[-4]
            assert aspect in ALL_ASPECTS
            save_file = '\\'.join([dp, f])
            all_aspects_files_dict[aspect].append(save_file)
            all_files.append(f)


#=====================
#== Plot distribution for each aspect.
#=====================

tmp = []
# all_aspects_data_dict = {i: [] for i in ALL_ASPECTS}
all_aspects_data_len_dict = {i: [] for i in ALL_ASPECTS}
# def _get_
for k,v in all_aspects_files_dict.items():
    len_data = 0
    for i in v:
        # print(v)
        # tmp.append(v)
        data = pickle.load(open(i, 'rb'))
        len_data += len(data['data'])
    all_aspects_data_len_dict[k] = len_data

    # all_aspects_data_dict[k].



