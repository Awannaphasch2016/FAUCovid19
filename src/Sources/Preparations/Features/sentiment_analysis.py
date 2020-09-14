#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Sentiment analysis."""

import nltk  # type: ignore
from textblob import TextBlob  # type: ignore


# OPTIMIZE: speed to this process ( takes way too long in comparison to
#  request)
def get_sentiment(text: str) -> float:
    """Get sentiment of a given text and return sentiment polarity.

    :type text: str
    :param text: any text

    :rtype: float
    :return: sentiment score range from 0 to 1
    """
    try:
        text_blob = TextBlob(text)
    except Exception as e:
        print(e)
        nltk.download("punkt")
        text_blob = TextBlob(text)

    text_blob = text_blob.correct()

    return text_blob.sentiment.polarity
