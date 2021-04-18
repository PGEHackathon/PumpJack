import numpy as np
import pandas as pd
import keras as kb
from sklearn.model_selection import train_test_split
from skelarn.preprocessing import StandardScaler
from tensorflow import keras
from keras.models import Sequential
from tensorflow.keras import layers
from keras.layers import Dense
from tensorflow.keras import regularizers
from tensorflow.keras import initializers


def create_model(n_inputs, n_outputs):
    model = Sequential()
    model.add(Dense(10, input_dim=n_inputs, kernel_initializer='he_uniform', activation = 'relu'))
    model.add(Dense(10, input_dim=n_inputs, kernel_initializer='he_uniform', activation='relu'))
    model.add(Dense(n_outputs))
    model.compile(loss='mae', optimizer='relu')
    return model


def data_split_year_1(well):
    X = well[column]
    y
    