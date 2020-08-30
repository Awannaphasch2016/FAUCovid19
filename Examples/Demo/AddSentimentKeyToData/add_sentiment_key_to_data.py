import numpy as np
from tqdm import tqdm_notebook as tqdm
import nltk
import pathlib
import pickle
import os
from textblob import TextBlob

# OPTIMIZE: speed to this process ( takes way too long in comparison to request)
def get_sentiment(text: str) -> float:
    """get sentiment of a given text and return sentiment polarity """
    try:
        text_blob = TextBlob(text)
    except:
        nltk.download('punkt')
        text_blob = TextBlob(text)

    text_blob = text_blob.correct()

    return text_blob.sentiment.polarity


def get_all_file(folder_path):
    import os
    for root, dirs, files in os.walk(folder_path, topdown=False):
        if root.split('/')[-1] == '2020-06-14-20-36-03-031482':
            for name in files:

                yield root, name

        # for name in dirs:
        #     print(os.path.join(root, name))


def get_sentiment_path(root):
    new_root = root.split('/')
    assert new_root[5] == 'with_tags', root
    new_root[5] = 'RedditWithSentiment'
    new_root = '/'.join(new_root)
    print(new_root)
    return new_root
    # folder_path = r'/content/gdrive/My Drive/Dataset/with_tags'
    # for root, dirs, files in os.walk(folder_path, topdown=False):
    #     if root.split('/')[-1] == '2020-06-14-20-36-03-031482':
    #       for name in files:
    #           # file_path = os.path.join(root, name)
    #           new_root = root.split('/')
    #           assert new_root[5] == 'with_tags', root
    #           new_root[5] = 'RedditWithSentiment'
    #           new_root = '/'.join(new_root)
    #           print(new_root)


def run():
    folder_path = r'/content/gdrive/My Drive/Dataset/with_tags'
    for (root, name) in tqdm(list(get_all_file(folder_path))[30:], desc='get_all_file'):

        file = os.path.join(root, name)
        f = pickle.load(open(file, 'rb'))
        content = f
        for i, res in tqdm(enumerate(f['data']), desc="f['data']"):

            all_text = []
            if res['selftext'] is not None:
                if isinstance(res['selftext'], str):
                    if len(res['selftext']) > 0:
                        all_text.append(res['selftext'])

            if res['title'] is not None:
                if isinstance(res['title'], str):
                    if len(res['title']) > 0:
                        all_text.append(res['title'])

            if res['body'] is not None:
                if isinstance(res['body'], str):
                    if len(res['body']) > 0:
                        all_text.append(res['body'])

            all_text_str = '.'.join(all_text)
            polarity = get_sentiment(all_text_str)
            # print(polarity)

            res['sentiment_polarity'] = polarity
            content['data'][i] = res
            print(polarity)

            assert 'sentiment_polarity' in content['data'][i]

        new_root = get_sentiment_path(root)
        print(new_root)
        print(name)

        save_file(content, name, new_root)

if __name__ == '__main__':
    pass
    # run()