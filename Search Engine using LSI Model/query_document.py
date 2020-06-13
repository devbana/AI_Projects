# Query Document Search Engine
# loading some necessary files
import os
import gensim
from gensim.models import LsiModel
from gensim import models
from gensim import corpora
from gensim.utils import lemmatize
import nltk
from nltk.stem import PorterStemmer
from gensim.parsing.preprocessing import remove_stopwords, stem_text
from gensim.parsing.preprocessing import strip_numeric
import pandas as pd
from gensim import similarities


# some pre-processing
def pre_processing():
    for document in cor:
        doc = strip_numeric(stem_text(document))
        yield gensim.utils.tokenize(doc, lower=True)


# path_corpus ='' for directory of Corpus
cor = pd.read_csv('cor_pus.txt', sep='\n', header=None)[0]
texts = pre_processing()
dictionary = corpora.Dictionary(texts)


dictionary.filter_extremes(no_below=1, keep_n=900)

doc_term_matrix = [dictionary.doc2bow(token) for token in pre_processing()]

tfidf = models.TfidfModel(doc_term_matrix)
corpus_tfidf = tfidf[doc_term_matrix]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=200)  # initialize an LSI transformation
doc = 'highest speed of plane'# Query
vec_bow = dictionary.doc2bow(doc.lower().split())

vec_lsi = lsi[vec_bow]  # convert the query to LSI space
index = similarities.MatrixSimilarity(lsi[doc_term_matrix])
unsorted_similarity = index[vec_lsi]
sorted_similarity = sorted(enumerate(unsorted_similarity), key=lambda item: -item[1])
tops = 0
print('Displaying top 10 records')
for index, similarity in sorted_similarity:
    if tops <= 10:
        print(similarity, cor[index])
        tops += 1
    else:
        break