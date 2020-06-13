from flask import Flask, request, jsonify, render_template
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
lemaoi = WordNetLemmatizer()
model_amazon = load_model('amazon.h5')
tokenizer = pickle.load(open('tokenizer_amazon.pickle','rb'))
max_len = 30
outp = {0: 'Neutral', 1: 'Positive', 2: 'Negative'}
app = Flask(__name__)


def pre_processing(x):
    x = x.lower()
    x = re.sub('[^a-z0-9 ]','',x)
    result = []
    for i in x.split():
        if i in stopwords.words('english'):
            pass
        else:
            if len(i) <3:
                pass
            else:
                result.append(lemaoi.lemmatize(i))
    res = ' '.join(result)
    res = re.sub('\d{2,}\w+','',res)
    return res


def word_sequence(x):
    sequen = tokenizer.texts_to_sequences(x)
    X = pad_sequences(sequen, maxlen=max_len)
    return X


def get_prob(pr_y):
    retu = False
    for i in pr_y[0]:
        if i >0.5:
            retu = True
    return retu


@app.route('/predict',methods=['POST'])
def predict():
    inpu = [i for i in request.form.values()]
    clean_input = pre_processing(inpu[0])
    # print(clean_input)
    X = word_sequence([clean_input])
    if get_prob(model_amazon.predict(X)):
        res = model_amazon.predict_classes(X)
        return render_template("index.html", prediction_text=outp[int(res)])
    else:
        return render_template("index.html", prediction_text_2="Sorry! not able to analyze that")


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()

'''
input_ = str(input('Enter Amazon Review\n'))
clean_input = pre_processing(input_)
#print(clean_input)
X = word_sequence([clean_input])
pred = model_amazon.predict(X)
res = model_amazon.predict_classes(X)
if get_prob(pred):
    print(outp[int(res)])
else:
    print('Sorry! not able to analyze that')'''