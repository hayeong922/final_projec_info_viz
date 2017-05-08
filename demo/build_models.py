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
# word2vec and pca part  of code was adopted from https://github.com/jdwittenauer/twitter-viz-demo


def main():

    corpus = corpus.map(lambda x: tokenize(x))
    word2vec = Word2Vec(corpus.tolist(), size=100, window=4, min_count=10, workers=4)
    word2vec.init_sims(replace=True)

    word_vectors = [word2vec[word] for word in word2vec.wv.vocab]  # in genism 1.0.0+ should use

    pca = PCA(n_components=2)
    pca.fit(word_vectors)

    joblib.dump(pca, path + 'pca.pkl')
    word2vec.save(path + 'word2vec.pkl')



if __name__ == "__main__":
    main()
