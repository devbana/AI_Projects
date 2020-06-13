import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from imutils import paths
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tensorflow.keras import models
from tensorflow.keras import layers
import build_model
import cv2 as cv

lis = ['paper','stone','scissors']
fix_path = r'C:\Users\HP\AI Projects\Learn\Kaggle\sps\rps\rps'
test_path = r'C:\Users\HP\AI Projects\Learn\Kaggle\sps\rps-test-set\rps-test-set'
imgpa =[]
for i in lis:
    #print(test_path + '\\' + i)
    imgpa.append(list(paths.list_images(fix_path + '\\' + i)))

'''
for i,j in enumerate(imgpa):
    for k in j:
        img_t = cv.imread(k)
        img_g = cv.cvtColor(img_t, cv.COLOR_BGR2GRAY)
        img_r = cv.resize(img_g, (28, 28))
        X.append(img_r)
x = np.array(X)
X_n = x.reshape(x.shape[0], 28, 28, 1)
'''
#print(X_n.shape)
# For Testing
obj = build_model.Build_SPS_Model('testting')
model_sps = obj.get_model()
img = cv.imread(r'C:\Users\HP\AI Projects\Learn\Kaggle\sps\rps-test-set\rps-test-set\rock\testrock03-01.png')
img_rgb = cv.cvtColor(img,cv.COLOR_BGR2RGB)
img_g = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_r = cv.resize(img_g, (28, 28))
x = np.array(img_r)
x = x.reshape(1,28,28,1)
res = model_sps.predict_classes(x)
print(model_sps.summary())
resul = lis[int(res)]
#print(resul)
font = cv.FONT_ITALIC
font_img = cv.putText(img_rgb,text=resul,org=(0,250),thickness=3,fontFace=font,fontScale=2,color=(255,0,0))
plt.imshow(font_img)
plt.show()
'''
for i in X_n:
    k = i.reshape(1,28,28,1)
    res = model_sps.predict_classes(k)
    print(lis[int(res)])
#print(int(rer))
#print(lis[int(rer)])

# For Training

y = np.array(Y)
Y_new = to_categorical(y)
print(Y_new.shape)
#print(X_n[0])
#plt.imshow(X_n[0].reshape(100,100))
#plt.show()
#x_train,x_test,y_train,y_test = train_test_split(X_n,Y_new,test_size=0.3)
obj = build_model.Build_SPS_Model(X_n,Y_new)
obj.build_model_keras()

'''