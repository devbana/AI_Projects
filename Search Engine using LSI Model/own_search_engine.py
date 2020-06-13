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
from nltk.tokenize import word_tokenize
from gensim import similarities
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
stop_nltk = stopwords.words('english')
vectorizer = TfidfVectorizer(max_features=3000)


def pre_processing():
    for document in texts:
        doc = strip_numeric(stem_text(document))
        yield gensim.utils.tokenize(doc, lower=True)


raw_data = pd.read_table("r8-all-terms.txt", sep="\t", names=['label', 'text'])
# seperate the texts from the dataframe
texts = raw_data['text'].values
tokenize_text = pre_processing()
dictionary = corpora.Dictionary(tokenize_text)
print('No of key value pair is {}'.format(max(dictionary.keys())))
dictionary.filter_extremes(no_below=1, keep_n=10000)
#dictionary.save('modeldic.dic')
doc_term_matrix = [dictionary.doc2bow(token) for token in pre_processing()]
tfidf = models.TfidfModel(doc_term_matrix)
corpus_tfidf = tfidf[doc_term_matrix]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=150)
lsi.save('lis_search.model')
doc = 'crude oil price'# Query
vec_bow = dictionary.doc2bow(doc.lower().split())

vec_lsi = lsi[vec_bow]  # convert the query to LSI space
index = similarities.MatrixSimilarity(lsi[doc_term_matrix])
'''
index.save('own_search_engine.index')

unsorted_similarity = index[vec_lsi]
sorted_similarity = sorted(enumerate(unsorted_similarity), key=lambda item: -item[1])
tops = 0
print('Displaying top 10 records')
for index, similarity in sorted_similarity:
    if tops <= 10:
        print(similarity, raw_data.loc[index, ['text']])
        tops += 1
    else:
        break
'''