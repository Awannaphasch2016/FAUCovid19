# x = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data\RedditCrawler\work_from_home\corona_countries\comment\data\after_date=2020-07-21_to_2020-08-20.pickle'
# --reddit
# x = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data\RedditCrawler\work_from_home\corona_countries\comment\data\after_date=2020-07-21_to_2020-08-20.pickle'
# --twitter
x = r'C:\Users\Anak\PycharmProjects\Covid19CookieCutter\Outputs\Data\TwitterCrawler\social_distance\twitter_tweet\data_tweet\data_tweet\after_date=2020-07-24_to_2020-07-25.pickle'


import pickle
import pprint
y = pickle.load(open(x, 'rb'))
pprint.pprint(y['metadata'].keys())
print()