from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense


def create_model_v1():
    keras_model = Sequential()
    keras_model.add(Conv2D(32, (3, 3), input_shape=(256,256,3)))
    keras_model.add(Activation('relu'))
    keras_model.add(MaxPooling2D(pool_size=(2, 2)))
    keras_model.add(Conv2D(32, (3, 3)))
    keras_model.add(Activation('relu'))
    keras_model.add(MaxPooling2D(pool_size=(2, 2)))
    keras_model.add(Conv2D(64, (3, 3)))
    keras_model.add(Activation('relu'))
    keras_model.add(MaxPooling2D(pool_size=(2, 2)))
    keras_model.add(Flatten())
    keras_model.add(Dense(64))
    keras_model.add(Activation('relu'))
    keras_model.add(Dropout(0.5))
    keras_model.add(Dense(3)) #3 classes
    keras_model.add(Activation('softmax'))
    return keras_model

def create_model_v2():
    keras_model = Sequential()
    keras_model.add(Conv2D(64, (3, 3), input_shape=(256,256,3)))
    keras_model.add(Activation('relu'))
    keras_model.add(MaxPooling2D(pool_size=(2, 2)))
    keras_model.add(Conv2D(64, (3, 3)))
    keras_model.add(Activation('relu'))
    keras_model.add(MaxPooling2D(pool_size=(2, 2)))
    keras_model.add(Conv2D(64, (3, 3)))
    keras_model.add(Activation('relu'))
    keras_model.add(MaxPooling2D(pool_size=(2, 2)))
    keras_model.add(Flatten())
    keras_model.add(Dense(256,activation='relu'))
    keras_model.add(Dropout(0.5))
    keras_model.add(Dense(256,activation='relu'))
    keras_model.add(Dropout(0.5))
    keras_model.add(Dense(3, activation='softmax')) #3 classes
    return keras_model

def create_model_v3():
    keras_model = Sequential()
    keras_model.add(Conv2D(64, (3, 3), input_shape=(256,256,3)))
    keras_model.add(Activation('relu'))
    keras_model.add(MaxPooling2D(pool_size=(2, 2)))
    keras_model.add(Conv2D(64, (3, 3)))
    keras_model.add(Activation('relu'))
    keras_model.add(MaxPooling2D(pool_size=(2, 2)))
    keras_model.add(Conv2D(64, (3, 3)))
    keras_model.add(Activation('relu'))
    keras_model.add(MaxPooling2D(pool_size=(2, 2)))
    keras_model.add(Conv2D(64, (3, 3)))
    keras_model.add(Activation('relu'))
    keras_model.add(MaxPooling2D(pool_size=(2, 2)))
    keras_model.add(Flatten())
    keras_model.add(Dense(64,activation='relu'))
    keras_model.add(Dropout(0.5))
    keras_model.add(Dense(3, activation='softmax')) #3 classes
    return keras_model

