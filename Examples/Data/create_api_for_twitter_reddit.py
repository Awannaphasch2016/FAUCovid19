import pickle
from pprint import pprint

# lockdown
lockdown_ex = 'C:/Users/Anak/PycharmProjects/Covid19CookieCutter/Outputs/Data/TwitterCrawler/twitter_tweet/data_tweet/lockdown/after_date=2020-07-24_to_2020-07-25.pickle'

# social_distance
social_distance_ex = 'C:/Users/Anak/PycharmProjects/Covid19CookieCutter/Outputs/Data/TwitterCrawler/twitter_tweet/data_tweet/social_distance/after_date=2020-07-30_to_2020-07-31.pickle'

def display_ex(x):
    for i,j in x.items():
        print(f'======={i}===========')
        if isinstance(j, list):
            # pprint(j[0])
            print(len(j))
        else:
            pprint(j)

display_ex(pickle.load(open(lockdown_ex, 'rb')))

display_ex(pickle.load(open(social_distance_ex, 'rb')))

