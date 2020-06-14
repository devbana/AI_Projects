#import tensorflow.keras
import os
import cv2 as cv
import numpy as np
from tensorflow.keras import layers
from tensorflow.keras import models


path = 'train_dataset/'
#print(os)


def prepare_dataset(path_):
    folders = os.listdir(path)
    X = []
    Y = []
    for i,j in enumerate(folders):
        images_ = os.listdir(path+j)
        for k in images_:
            img_ = cv.imread(path+j+'/'+k,cv.IMREAD_GRAYSCALE)
            img_= cv.resize(img_,(100,100))
            #img_c = cv.cvtColor(img_,cv.COLOR_BGR2RGB)
            #img_g = cv.cvtColor(img_c,cv.COLOR_RGB2GRAY)
            X.append(img_)
            Y.append(i)  
    return X,Y
        #cv.imshow('Image',img_)


x,y = prepare_dataset(path)
Y_train = np.array(y)
# shaping the data
x_train = np.array(x)
x_train = x_train/255
X_train = x_train.reshape(x_train.shape[0],100,100,1)


face_model = models.Sequential()
face_model.add(layers.Conv2D(64,kernel_size=3,input_shape=(100,100,1),activation='relu'))

face_model.add(layers.Conv2D(400,kernel_size=3,activation='relu'))
face_model.add(layers.MaxPool2D(pool_size=(2,2)))

face_model.add(layers.Conv2D(600,kernel_size=3,activation='relu'))
face_model.add(layers.MaxPool2D(pool_size=(2,2)))

face_model.add(layers.Conv2D(250,kernel_size=3,activation='relu'))
face_model.add(layers.MaxPool2D(pool_size=(2,2)))

face_model.add(layers.Conv2D(100,kernel_size=3,activation='relu'))
face_model.add(layers.MaxPool2D(pool_size=(2,2)))

face_model.add(layers.Flatten())
face_model.add(layers.Dense(50,activation='relu'))
face_model.add(layers.Dense(1,activation='sigmoid'))
face_model.compile(optimizer='Adam',metrics=['acc'],loss='binary_crossentropy')
face_model.fit(X_train,Y_train,batch_size=20, epochs=10)
print(face_model.summary())
face_model.save('face_model.h5')
