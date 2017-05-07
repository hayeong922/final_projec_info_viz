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
import csv


from textblob import TextBlob



# the code was adopted from https://github.com/jdwittenauer/twitter-viz-demo and made slight change


# Load transforms and models
vectorizer = joblib.load(path + 'vectorizer.pkl')
classifier = joblib.load(path + 'classifier.pkl')
pca = joblib.load(path + 'pca.pkl')
word2vec = Word2Vec.load(path + 'word2vec.pkl')




def classify_tweet(tweet):
    """
    Classify a tweet with either a positive (1) or negative (0) sentiment.
    Poliarity score between 0 to 1 postive, -1 to 0 negativce
    """

    text = str(tweet.encode('ascii','ignore'))

    blob = TextBlob(text)
    sent = blob.sentiment.polarity

    # print('original',text)
    # print('text',blob)
    # print('sentiment',sent)

    if sent > 0 and sent <= 1:
        return 1,text
    elif sent >= -1 and sent<=0:
        return 0,text


    # print('classify',tweet)
    # print('classify text',tweet.text)
    # print('classify text list',[tweet.text])
    # print('np.array',np.array([tweet.text]))
    # # test, original
    # print('np.array',np.array([tweet.text]),type(np.array([tweet.text])), type([tweet.text]),type(tweet.text))
    # print('vecotorizer',vectorizer.transform(np.array([tweet.text])))
    #
    # pred = classifier.predict(vectorizer.transform(np.array([tweet.text])))
    # print('pred',pred)
    #
    # return str(pred[0])


    # # # print('tweet',type(tweet),tweet)
    # # # print('tweet np array',type(np.array([tweet])),np.array([tweet]))
    # pred = classifier.predict(vectorizer.transform(list))
    # # input = str(tweet.encode('ascii','ignore'))
    # # #input = input.split()
    # # print('input',input)
    # # print('type',type(input))
    # # pred = classifier.predict(vectorizer.transform(input))
    # # #
    # # #pred = classifier.predict(vectorizer.transform(np.array(tweet['text'])))
    # # #
    # # # print('classify done')
    # # #
    # # # print('a',str(pred[0]))
    # # #
    # return str(pred[0])


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

    return str(x), str(y)


def create_stream():
    """
    Celery task that connects to the twitter stream and runs a loop, periodically
    emitting tweet information to all connected clients.
    """
    senti_list = []
    text_list = []
    x_list = []
    y_list = []


    count = 0
    with open('./data/collect_zika.json', 'r') as f:
        for line in f:
            tweet = json.loads(line)
            sentiment, words = classify_tweet(tweet['text'])
            senti_list.append(sentiment)
            text_list.append(words)
            x, y = vectorize_tweet(tweet['text'])
            x_list.append(x)
            y_list.append(y)
            count +=1

    print('count',count)
    f = open('./data/sentiment.csv', 'wt')
    try:
        writer = csv.writer(f)
        writer.writerow(('x', 'y', 'senti', 'text'))
        for i in range(0,count):
            writer.writerow((x_list[i], y_list[i], senti_list[i], text_list[i]))
    finally:
        f.close()


if __name__ == '__main__':
    create_stream()

