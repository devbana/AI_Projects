import cv2 as cv
import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import models, layers
output = {0:'Akash',1:'Sonali'}
from tensorflow.keras.models import load_model
model_face = load_model('face_model.h5')
img_ = cv.imread(r'C:\Users\HP\AI Projects\Learn\face_detection\train_dataset\Sonali\4.jpg',cv.IMREAD_GRAYSCALE)
img_g = cv.resize(img_,(100,100))
img_n = np.resize(img_g,(1,100,100,1))
print(img_n.shape)
rss_1 = model_face.predict(img_n)
res = model_face.predict_classes(img_n)
print(res[0])
print(output[int(res[0])])

#cv.imshow('Akash',img_g)
#cv.waitKey(500)

