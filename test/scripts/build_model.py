import os
import sys
path = os.path.realpath('') + '/'
sys.path.append(path)

import pandas as pd
from sklearn.decomposition.pca import PCA
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from gensim.models import Word2Vec
from tokenizer import *


def main():
    print('Reading data file')
    data = pd.read_csv(path + 'Sentiment Analysis Dataset.csv',
                       usecols=['Sentiment', 'SentimentText'], error_bad_lines=False)

    print('Preprocess')
    corpus = data['SentimentText']
    vectorizer = TfidfVectorizer(decode_error='replace', strip_accents='unicode',
                                 stop_words='english', tokenizer=tokenize)
    X = vectorizer.fit_transform(corpus.values)
    y = data['Sentiment'].values

    print('Train sentiment classification')
    classifier = MultinomialNB()
    classifier.fit(X, y)

    print('Word2Vec')
    corpus = corpus.map(lambda x: tokenize(x))
    word2vec = Word2Vec(corpus.tolist(), size=100, window=4, min_count=10, workers=4)
    word2vec.init_sims(replace=True)

    print('Fitting 2 PCA')
    #word_vectors = [word2vec[word] for word in word2vec.vocab] # pre -1.0.0
    word_vectors = [word2vec[word] for word in word2vec.wv.vocab]  # in genism 1.0.0+ should use

    pca = PCA(n_components=2)
    pca.fit(word_vectors)

    # print('Saving artifacts to disk...')
    # joblib.dump(vectorizer, path + 'vectorizer.pkl')
    # joblib.dump(classifier, path + 'classifier.pkl')
    # joblib.dump(pca, path + 'pca.pkl')
    # word2vec.save(path + 'word2vec.pkl')
    #
    # print('Done')


if __name__ == "__main__":
    main()
