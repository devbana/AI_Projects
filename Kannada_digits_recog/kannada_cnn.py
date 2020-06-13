import tensorflow
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import Sequential
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import layers
import matplotlib.pyplot as plt
# getting the data
raw_data_y = pd.read_csv('test.csv')
raw_data_y.drop('id',axis=1,inplace=True)
'''
raw_data = pd.read_csv('train.csv')

y = raw_data['label']
y = to_categorical(y)
raw_data.drop('label',axis=1,inplace=True)

x = np.array(raw_data)
x = x.reshape(x.shape[0],28,28,1)
x = x/255
'''
test_data = np.array(raw_data_y)
test_data = test_data.reshape(test_data.shape[0],28,28,1)
test_data = test_data/255
#print(Y)
# Scaling the values
#x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)
model_cnn = load_model('model_kannada_cnn.h5')
#model_cnn.summary()
y_pred = model_cnn.predict_classes(test_data)
raw_data_y['pred'] = y_pred
raw_data_y.to_csv('sample_sub.csv')
'''
model_cnn_ken = Sequential()
model_cnn_ken.add(layers.Conv2D(128,kernel_size=(3,3),input_shape=(28,28,1), activation='relu'))
model_cnn_ken.add(layers.MaxPool2D(pool_size=(2,2)))
model_cnn_ken.add(layers.Conv2D(64,kernel_size=(2,2), activation='relu'))
model_cnn_ken.add(layers.MaxPool2D(pool_size=(2,2)))
model_cnn_ken.add(layers.Conv2D(20,kernel_size=(2,2), activation='relu'))
model_cnn_ken.add(layers.Flatten())
model_cnn_ken.add(layers.Dense(50,activation='relu'))
model_cnn_ken.add(layers.Dense(10,activation='softmax'))
model_cnn_ken.compile(optimizer='Adam',metrics=['acc'],loss='categorical_crossentropy')
model_cnn_ken.fit(x_train,y_train,batch_size=500, epochs=10)
model_cnn_ken.evaluate(x_test,y_test)
model_cnn_ken.save('model_kannada_cnn.h5')
'''

