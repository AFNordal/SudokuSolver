from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras import backend as K
K.set_image_dim_ordering('th')
from keras import optimizers
from keras import metrics
from keras.datasets import mnist
from keras.utils import np_utils
import numpy as np
from matplotlib import pyplot
from keras.models import load_model
from keras.models import save_model
np.random.seed(7)


def baseNet():
    model=Sequential()
    model.load_weights('weights.h5')
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    return model

def readSudoku(sud):
    net=baseNet()
    result=np.empty(81)
    tarr=sud.reshape(81,1,28,28)
    predictions=net.predict_on_batch(tarr)
    for i in range(81):
        result[i]=np.argmax(predictions[i])
    return result
     