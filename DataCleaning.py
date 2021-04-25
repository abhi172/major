import numpy as np
import re


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt


def clean_tweets(tweet):
    # remove twitter Return handles (RT @xxx:)
    tweet = np.vectorize(remove_pattern)(tweet, "RT @[\w]*:")

    # remove twitter handles (@xxx)
    tweet = np.vectorize(remove_pattern)(tweet, "@[\w]*")

    # remove URL links (httpxxx)
    tweet = np.vectorize(remove_pattern)(tweet, "https?://[A-Za-z0-9./]*")

    # remove special characters, numbers, punctuations (except for #)
    tweet = np.core.defchararray.replace(tweet, "[^a-zA-Z]", " ")

    return tweet

