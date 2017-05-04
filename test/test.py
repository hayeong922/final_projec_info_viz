import os
import sys
path = os.path.realpath('') + '/scripts/'
sys.path.append(path)

import time
import numpy as np
# flask import *
from pattern.web import Twitter
from sklearn.externals import joblib
from gensim.models import Word2Vec
from tokenizer import *
import json


# the code was adopted from https://github.com/jdwittenauer/twitter-viz-demo and made slight change


# Load transforms and models
vectorizer = joblib.load(path + 'vectorizer.pkl')
classifier = joblib.load(path + 'classifier.pkl')
pca = joblib.load(path + 'pca.pkl')
word2vec = Word2Vec.load(path + 'word2vec.pkl')


def classify_tweet(tweet):
    """
    Classify a tweet with either a positive (1) or negative (0) sentiment.
    """
    #print('tweet',type(tweet),tweet)
    #print('tweet np array',type(np.array([tweet])),np.array([tweet]))
    #pred = classifier.predict(vectorizer.transform(np.array([tweet])))
    input = str(tweet.encode('ascii','ignore'))
    input = input.split()
    print('input',input)
    #print('type',type(input))
    pred = classifier.predict(vectorizer.transform([input]))

    #pred = classifier.predict(vectorizer.transform(np.array(tweet['text'])))

    print('classify done')

    print('a',str(pred[0]))

    return str(pred[0])


def vectorize_tweet(tweet):
    """
    Convert a tweet to vector space using a pre-trained word2vec model, then transform
    a sum of the vectorized words to 2-dimensional space using PCA to give a simple
    2D coordinate representation of the original tweet.
    """
    tweet_vector = np.zeros(100)
    for word in tokenize(tweet):
        if word in word2vec.wv.vocab:
            tweet_vector = tweet_vector + word2vec[word]

    components = pca.transform(tweet_vector)
    x = components[0, 0]
    y = components[0, 1]

    print('vectorize done')

    return str(x), str(y)


def create_stream():
    """
    Celery task that connects to the twitter stream and runs a loop, periodically
    emitting tweet information to all connected clients.
    """

    with open('data/collect_zika.json', 'r') as f:
        for line in f:
            tweet = json.loads(line)
            sentiment = classify_tweet(tweet['text'])
            x, y = vectorize_tweet(tweet['text'])
            #print('x,y',x,y)
            # print('tweet', {'id': w['id'],
            #                      'text': w['text'],
            #                      'sentiment': sentiment,
            #                      'x': x,
            #                      'y': y})
        time.sleep(1)



if __name__ == '__main__':
    create_stream()
