# x = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data\RedditCrawler\work_from_home\corona_countries\comment\data\after_date=2020-07-21_to_2020-08-20.pickle'
# --reddit
# x = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data\RedditCrawler\work_from_home\corona_countries\comment\data\after_date=2020-07-21_to_2020-08-20.pickle'
#   C:\\Users\\Anak\\PycharmProjects\\Covid19CookieCutter\\Outputs\\Data\\RedditCrawler\\work_from_home\\corona_countries\\comment\\after_date=2020-07-22_to_2020-08-21.pickle
# x = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data\RedditCrawler\work_from_home\corona_countries\comment\data\after_date=2020-07-22_to_2020-08-21.pickle'
# --twitter
x = r"C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data\TwitterCrawler\social_distance\twitter_tweet\data_tweet\data_tweet\after_date=2020-07-24_to_2020-07-25.pickle"

import pickle
import pprint

y = pickle.load(open(x, "rb"))
# pprint.pprint(y)
# pprint.pprint(y['data'][0].keys())
# pprint.pprint(y['aggs']['created_utc'])
# pprint.pprint(y['metadata'].keys())
# pprint.pprint(y['metadata']['running_constraints'])

# pprint.pprint(y['data'][0]['link_id'])
# pprint.pprint(y['data'][0]['parent_id'])
# pprint.pprint(y['data'][0]['id'])

# pprint.pprint(y['metadata'].keys())
# pprint.pprint(y['metadata']['subreddit'])
print()

# from os import listdir
# from os.path import isfile, join

# # mypath = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data\RedditCrawler'
# mypath = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs'
# from os import walk

# f = []
# for (dirpath, dirnames, filenames) in walk(mypath):
#     f.extend(filenames)
# print(f)

# import os
# result = [ f for dp, dn, filenames in os.walk(mypath) for f in filenames if os.path.splitext(f)[1] == '.pickle']
# print(result)
