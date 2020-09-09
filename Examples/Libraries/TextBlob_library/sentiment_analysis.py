from textblob import TextBlob
import nltk
from tqdm import tqdm

nltk.download("punkt")

text = "i am 😞"  # emoji sentiment.polarity = 0
text = "I hate going to school"
text = "I am tyyping it wrong on purrpose"


for i in tqdm(range(100)):
    wiki = TextBlob(text)

wiki = TextBlob(text)

wiki = wiki.correct()  # correcct the misspelling

wiki.tags

wiki.noun_phrases

wiki.sentiment

wiki.sentiment.polarity
