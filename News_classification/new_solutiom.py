import pandas
import tensorflow.keras.models as model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
ouput = {0:'Business', 1:'Entertainment', 2:'Health',3:'Science and Technology'}
query = input('please enter query:\n')


def get_seq(x):
    max_len = 130
    tokenizer = pickle.load(open('tokenizer.pickle','rb'))
    sequences = tokenizer.texts_to_sequences([x])
    X = pad_sequences(sequences, maxlen=max_len)
    return X

x = get_seq(query)
model_new = model.load_model('multiclass_model.h5')
res1 = model_new.predict(x)
oup = [True if i > 0.5 else False for i in res1[0] ]
if oup is True:
    res = model_new.predict_classes(x)
    print(ouput[int(res[0])])
else:
    print('Sorry! not trained on this data ')

#res = model_new.predict_classes(x)
#print(ouput[int(res[0])])