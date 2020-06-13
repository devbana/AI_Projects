from sklearn.model_selection import train_test_split
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras.models import load_model

class Build_SPS_Model:
    def __init__(self,x,y):
        self.X = x
        self.Y = y

    def __init__(self,strx):
        pass

    def get_model(self):
        model_sps = load_model('sps_model.h5')
        return model_sps


    def build_model_keras(self):
        x_train, x_test, y_train, y_test = train_test_split(self.X, self.Y, test_size=0.3)
        sps_model = models.Sequential()
        sps_model.add(layers.Conv2D(64,kernel_size=(3,3),activation='relu',input_shape=(28,28,1)))
        sps_model.add(layers.Conv2D(32,kernel_size=(3,3),activation='relu'))
        sps_model.add(layers.MaxPool2D(pool_size=(2, 2), strides=1))
        sps_model.add(layers.Flatten())
        sps_model.add(layers.Dense(128,activation='relu'))
        sps_model.add(layers.Dropout(0.2))
        sps_model.add(layers.Dense(3,activation='softmax'))
        sps_model.compile(optimizer='adam',loss=losses.categorical_crossentropy, metrics=['acc'])
        sps_model.fit(x_train,y_train,epochs=10,batch_size=200)
        sps_model.evaluate(x_test,y_test)
        sps_model.save('sps_model.h5')


