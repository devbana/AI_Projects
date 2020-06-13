from tensorflow.keras import layers
from tensorflow.keras import models


def buildmodel(n_unique_words, shape_1):
    model = models.Sequential()
    model.add(layers.Embedding(n_unique_words, 130, input_length=shape1))
    model.add(layers.SpatialDropout2D(0.7))
    model.add(layers.LSTM(64, dropout=0.2, recurrent_dropout=0.3))
    model.add(layers.Dense(4, activation='softmax'))
    model.fit()
