import nltk
from textblob import TextBlob


# optimize: speed to this process ( takes way too long in comparison to request)
def get_sentiment(text: str) -> float:
    """get sentiment of a given text and return sentiment polarity """
    try:
        text_blob = TextBlob(text)
    except:
        nltk.download('punkt')
        text_blob = TextBlob(text)

    text_blob = text_blob.correct()

    return text_blob.sentiment.polarity
