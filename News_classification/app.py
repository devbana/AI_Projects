from flask import Flask, request, jsonify, render_template
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import tensorflow.keras.models as model
app = Flask(__name__)
output = {0:'Business', 1:'Entertainment', 2:'Health',3:'Science and Technology'}
tokenizer = pickle.load(open('tokenizer.pickle','rb'))
model_new = model.load_model('multiclass_model.h5')


def get_oup(op):
    resu = False
    for i in op[0]:
        if i > 0.5:
            resu =True
    return resu


def get_seq(x):
    max_len = 130
    #tokenizer = pickle.load(open('tokenizer.pickle','rb'))
    sequences = tokenizer.texts_to_sequences([x])
    X = pad_sequences(sequences, maxlen=max_len)
    return X


@app.route('/predict',methods=['POST'])
def predict():
    inpu = [i for i in request.form.values()]
    #print(inpu[0])
    x = get_seq(inpu[0])
    oup = get_oup(model_new.predict(x))
    #print(oup)
    if oup is True:
        res = model_new.predict_classes(x)
        #ouop = 'News Header  "{}", classified as {}'.format(inpu[0],res)
        return render_template("index.html",prediction_text=output[int(res)])
    else:
        return render_template("index.html", prediction_text_2="Sorry! not trained on this data ")


@app.route('/')
def home():
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=False)