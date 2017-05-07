import pandas
import json
from nltk.tokenize import word_tokenize
import re
import csv
import sys


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

tweet_text = []
count = 0
with open('data/collect_zika.json','r') as f:
    for line in f:
        tweet = json.loads(line)

        dates_zika.append(tweet['created_at'])
        tweet_text.append(1)
        count+=1

print 'count',count



f = open('./data/time_series.csv', 'wt')
try:
    writer = csv.writer(f)
    writer.writerow(('date', 'text'))
    for i in range(count):
        writer.writerow((dates_zika[i].encode("utf-8"), tweet_text[i]))
finally:
    f.close()

#print open('./data/time_series.csv', 'rt').read()


# this is the part for counting per minute or hours
 # a list of "1" to count the hashtags
#ones = [1] * len(dates_zika)
#
# # the index of the series
#idx = pandas.DatetimeIndex(dates_zika)
# # the actual series (at series of 1s for the moment)
#zika = pandas.Series(ones, index=idx)
#
# # Resampling / bucketing
#per_minute = ITAvWAL.resample('15Min', how='sum').fillna(0)
#per_minute = zika.resample('30Min').sum().fillna(0)
#print 'per minute'
# print per_minute

