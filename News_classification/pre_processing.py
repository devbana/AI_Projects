import numpy as mp
from tensorflow.keras.models import load_model
import pandas as pd
import pickle
from tensorflow.keras import layers
from tensorflow.keras import models
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.utils import shuffle
raw_data =pd.read_csv('uci-news-aggregator.csv')
#print(raw_data['CATEGORY'].value_counts())
print('As we can see the data is not balanced here so are making a balanced dataset')
ouput = {0:'Business', 1:'Entertainment', 2:'Health',3:'Science and Technology'}
shuffled = shuffle(raw_data)
shuffled.reset_index(inplace=True)
shuffled.drop('index', axis=1, inplace= True)
e = shuffled[shuffled['CATEGORY'] == 'e'][:45000]
b = shuffled[shuffled['CATEGORY'] == 'b'][:45000]
t = shuffled[shuffled['CATEGORY'] == 't'][:45000]
m = shuffled[shuffled['CATEGORY'] == 'm'][:45000]
new_dataset = pd.concat([e,b,t,m])
#new_dataset.to_excel('training.xlsx')
new_dataset.reset_index(inplace=True)
new_dataset['CATEGORY'].replace({'b':0, 'e':1,'m':2,'t':3}, inplace=True)
new_dataset.drop('index', axis=1, inplace= True)
#print(new_dataset.columns)
Y = new_dataset['CATEGORY']
Y = to_categorical(Y)
#train_ = new_dataset.loc[:,['TITLE','CATEGORY']]
#train_.to_excel('train_dataset.xlsx')
n_most_common_words = 50000
tokenizer = Tokenizer(num_words=n_most_common_words, filters='!"#$%&()*+-=<>?@[\]_:{|}~`', lower=True)
tokenizer.fit_on_texts(new_dataset['TITLE'].values)
sequences = tokenizer.texts_to_sequences(new_dataset['TITLE'].values)
word_index = tokenizer.word_index
#print(word_index)
max_len = 130
print('Found %s unique tokens.'%len(word_index))
X = pad_sequences(sequences, maxlen=max_len)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=45)
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

model = models.Sequential()
model.add(layers.Embedding(n_most_common_words,130, input_length=x_train.shape[1]))
model.add(layers.LSTM(64, dropout=0.2))
model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(4, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
model.fit(x_train, y_train, epochs=10, batch_size=1000)

print(model.evaluate(x_test, y_test))
print(model.summary())
model.save('multiclass_model.h5')

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
