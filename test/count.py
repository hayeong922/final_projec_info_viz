import pandas
import json
#import vincent
from nltk.tokenize import word_tokenize
import re
from collections import Counter
from collections import defaultdict
import math
import operator
import json
from collections import Counter
from nltk.corpus import stopwords
import string

dates_zika = []
# f is the file pointer to the JSON data set

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

#with open('data/stream_zika.json','r') as f:
print ''
print ''
print '*******Data loaded!********'

print 'dates'
tweet_count = 0
with open('data/collect_zika.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        tweet_count +=1
        # let's focus on hashtags only at the moment
        #terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
        terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('zika')]

        # track when the hashtag is mentioned
        #if '#zika' in terms_hash:
        if 'zika' in terms_hash:
            dates_zika.append(tweet['created_at'])
            #print dates_zika

print 'tweet_count',tweet_count

