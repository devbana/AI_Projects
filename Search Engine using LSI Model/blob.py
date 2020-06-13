from flask import Flask, request, jsonify, render_template
import gensim
from gensim.models import LsiModel
from gensim import corpora
from gensim.parsing.preprocessing import remove_stopwords, stem_text
from gensim.parsing.preprocessing import strip_numeric
import pandas as pd
from gensim import similarities
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
raw_data = pd.read_table("r8-all-terms.txt", sep="\t", names=['label', 'text'])
model_lsi = LsiModel.load('lis_search.model')
dict = corpora.Dictionary.load('modeldic.dic')
index_ = similarities.Similarity.load('own_search_engine.index')
stop_nltk = stopwords.words('english')
vectorizer = TfidfVectorizer(max_features=3000)
app = Flask(__name__)

def pre_processing():
    for document in texts:
        doc = strip_numeric(stem_text(document))
        yield gensim.utils.tokenize(doc, lower=True)


def get_resul(z):
    vec_bow = dict.doc2bow(z.lower().split())
    vec_lsi = model_lsi[vec_bow]
    unsorted_similarity = index_[vec_lsi]
    sorted_similarity = sorted(enumerate(unsorted_similarity), key=lambda item: -item[1])
    tops = 0
    result = ''
    for index, similarity in sorted_similarity:
        if tops <= 5:
            resul = raw_data.loc[index, ['text']]
            result = result + str(float(similarity) * 100) + ' ' + str(raw_data.loc[index, ['text']][0])
            result = result +'\n'
            # print(, raw_data.loc[index, ['text']][0])
            tops += 1
        else:
            break
    return result


@app.route('/predict',methods=['POST'])
def predict():
    inpu = [i for i in request.form.values()]
    res = get_resul(inpu[0])
    return render_template("index.html", prediction_text=res)


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
