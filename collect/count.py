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

# # Removing stop-words
# punctuation = list(string.punctuation)
# stop = stopwords.words('english') + punctuation + ['rt','via']
#
# # count single term with counter
# with open('data/zika.json', 'r') as f:
#     count_all = Counter()
#     for line in f:
#         tweet = json.loads(line)
#         # create a list with all the terms
#         #terms_all = [term for team in preprocess(tweet['text'])]
#         terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
#         # update the counter
#         count_all.update(terms_stop)
#     #print the first 5 most frequent words
#     print 'single term frequence',(count_all.most_common(5))
#
# # update terms without stop words
#
#
# ### sentiment analysis part
# # compute probability
# # n_docs is the total n. of tweets
#
# # com: co-occurence was stored
# # count_stop_single(which does not store stop-words)
#
# # co-occurence
# com = defaultdict(lambda : defaultdict(int))
#
# # f is the file pointer to the JSON data set
# with open('data/zika.json', 'r') as f:
#     for line in f:
#         tweet = json.loads(line)
#         terms_only = [term for term in preprocess(tweet['text'])
#                       if term not in stop
#                       and not term.startswith(('#','@'))]
#
#         # Build co-occurrence matrix
#         for i in range(len(terms_only)-1):
#             for j in range(i+1,len(terms_only)):
#                 w1,w2 = sorted([terms_only[i],terms_only[j]])
#                 if w1 != w2:
#                     com[w1][w2] += 1
#
# print ' '
# print 'co-occurence'
# com_max = []
# # for each term, look for the most common co-occurrent terms
# for t1 in com:
#     t1_max_terms = sorted(com[t1].items(),key=operator.itemgetter(1),reverse=True)[:5]
#     for t2,t2_count in t1_max_terms:
#         com_max.append(((t1,t2),t2_count))
#     # Get the most frequent co-occurrences
#     terms_max = sorted(com_max,key=operator.itemgetter(1),reverse=True)
# print (terms_max[:5])
# print ' '
#
#
#
#
# count_stop_single = {}
# count_stop_single = count_all
# #print 'type count_strop singel',type(count_stop_single)
# #print 'type terms_stop',type(terms_stop)
# #print 'terms_stop',terms_stop
#
#
#
# p_t = {}
# p_t_com = defaultdict(lambda: defaultdict(int))
# n_docs = tweet_count
#
# for term, n in count_stop_single.items():
#     p_t[term] = float(n) / float(n_docs)
#     for t2 in com[term]:
#         p_t_com[term][t2] = float(com[term][t2])/float(n_docs)
#
#
#
# #print 'p_t',p_t
# # compute semantic orientation
# # given two vocab for positives and negative terms
# positive_vocab = ['good','nice','great','awesome','outstanding',
#     'fantastic', 'terrific', ':)', ':-)', 'like', 'love']
#
# negative_vocab = ['bad','terrible','crap','useless','hate',':(', ':-(']
#
# # can compute PMI of each pair of term
# # and then compute the Semantic Orientation
# pmi = defaultdict(lambda : defaultdict(int))
# for t1 in p_t:
#     for t2 in com[t1]:
#         denom = p_t[t1] * p_t[t2]
#         #pmi[t1][t2] = math.log2(p_t_com[t1][t2]/denom)
#         #print 'denom',denom
#         #print 'p_t[1]',p_t[t1]
#         #print 'p_t[2]',p_t[t2]
#
#         pmi[t1][t2] = math.log(p_t_com[t1][t2]/denom)
#
#
# semantic_orientation = {}
# for term, n in p_t.items():
#     positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
#     negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
#     semantic_orientation[term] = positive_assoc - negative_assoc
#
# semantic_sorted = sorted(semantic_orientation.items(),
#                          key=operator.itemgetter(1),
#                          reverse=True)
# top_pos = semantic_sorted[:10]
# top_neg = semantic_sorted[-10:]
#
# print 'top positive'
# print(top_pos)
# print ' '
#
# print 'top negative'
# print(top_neg)
# print ' '
# #print("#ITA: %f" % semantic_orientation['#ita'])
# #print("#FRA: %f" % semantic_orientation['#fra'])
#
# print 'sentiment analysis'
# print("zika: %f" % semantic_orientation['zika'])
# print("Zika: %f" % semantic_orientation['Zika'])
# print("birth: %f" % semantic_orientation['birth'])
#
# # a list of "1" to count the hashtags
# ones = [1] * len(dates_zika)
#
# # the index of the series
# idx = pandas.DatetimeIndex(dates_zika)
# # the actual series (at series of 1s for the moment)
# zika = pandas.Series(ones, index=idx)
#
# # Resampling / bucketing
# per_minute = zika.resample('1Min').sum().fillna(0)
# #print 'per minute'
# #print per_minute
#
# time_chart = vincent.Line(per_minute)
# time_chart.axis_titles(x='Time', y='Freq')
# #time_chart.to_json('stream_zika.json', html_out=True, html_path='chart.html')
# time_chart.to_json('merged.json', html_out=True, html_path='merged.html')
#
# fname = 'data/zika.json'
#
# with open(fname, 'r') as f:
#     count_all = Counter()
#     for line in f:
#         tweet = json.loads(line)
#         # Create a list with all the terms
#         terms_all = [term for term in preprocess(tweet['lang'])]
#         # Update the counter
#         count_all.update(terms_all)
#     # Print the first 5 most frequent words
#
# #word_freq = count_terms_only.most_common(20)
# word_freq = count_all.most_common(5)
# #print 'lang_freq'
# #print word_freq
#
# labels, freq = zip(*word_freq)
# data = {'data': freq, 'x': labels}
# bar = vincent.Bar(data, iter_idx='x')
# #bar.to_json('term_freq.json')
#bar.to_json('merged2.json', html_out=True, html_path='merged.html')