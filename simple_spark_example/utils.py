__author__ = 'jchugh'

import re

valid = re.compile("\w", re.UNICODE)

def extract_hashtags(tweet):
    """
    Extracts the hashtags from a tweet
    :param tweet: the tweet
    :type tweet: str
    :return: a set of hashtags
    :rtype: set of str
    """
    x = ""
    y = set()
    in_hash = False
    for c in tweet:
        if in_hash and not valid.match(c):
            if len(x) > 1:
                y.add(x)
            in_hash = False
            x = ""
        elif in_hash and valid.match(c):
            x += c.upper()
        if c == '#':
            x += c
            in_hash = True

    if len(x) > 1:
        y.add(x)
    return y
