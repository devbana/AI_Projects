import tensorflow
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import layers
import matplotlib.pyplot as plt
# getting the data

raw_data = pd.read_csv('train.csv')
raw_data_y = pd.read_csv('test.csv')
y = raw_data['label']
y = to_categorical(y)
raw_data.drop('label',axis=1,inplace=True)
raw_data_y.drop('id',axis=1,inplace=True)
x = np.array(raw_data)
x = x/255
test_data = np.array(raw_data_y)
test_data = test_data/255
#print(Y)
# Scaling the values
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)
model_dense = Sequential()
model_dense.add(layers.Dense(300, input_dim=x_train.shape[1],activation='relu'))
model_dense.add(layers.Dropout(0.2))
model_dense.add(layers.Dense(100,activation= 'relu'))
model_dense.add(layers.Dense(10,activation= 'softmax'))
model_dense.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
model_dense.fit(x_train,y_train, batch_size=1000, epochs=20)
model_dense.summary()
model_dense.save('model_kannada_dense.h5')
model_dense.evaluate(x_test,y_test)


