import numpy as np, joblib

from matplotlib import pyplot as plt

from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from sklearn.model_selection import train_test_split

from keras.models import Sequential, load_model
from keras.layers import Dense,Conv1D, Conv2D, MaxPooling2D, Flatten, Dropout, MaxPooling1D, GlobalAveragePooling1D
from keras.utils import to_categorical

class FinNN:
    def __init__(self, nn_type="ANN"):
        self.x, self.x_test = None, None
        self.y, self.y_test = None, None
        self.scale_x = None
        self.scale_y = None
        self.model = Sequential()
        self.predictions = None
        self.nn_type = nn_type
        self.categorical = False

    def setTestData(self, x, y):
        x = self.my_reshape(x)
        y = self.my_reshape(y)
        if self.nn_type == "CNN2D":
            x = np.expand_dims(x, axis=3)
        elif self.nn_type == "CNN1D":
            x = np.expand_dims(x, axis=2)
        self.x_test, self.y_test = x, y
        
    def setData(self, x, y, test_size=1):
        x = self.my_reshape(x)
        y = self.my_reshape(y)
        if self.nn_type == "CNN2D":
            x = np.expand_dims(x, axis=3)
        elif self.nn_type == "CNN1D":
            x = np.expand_dims(x, axis=2)
        self.x, self.x_test, self.y, self.y_test = train_test_split(x, y, test_size=test_size)
         
    def my_reshape(self, x):
        if self.nn_type == "ANN":
            if len(x.shape) == 1:
                x = x.reshape(len(x), 1)
            else:
                x = x.reshape(len(x), len(x[0]))
        return x

    def normalize(self):
        self.scale_x = MinMaxScaler()
        self.scale_y = MinMaxScaler()
        self.x = self.scale_x.fit_transform(self.x)
        self.x_test = self.scale_x.transform(self.x_test)
        self.y = self.scale_y.fit_transform(self.y)
        self.y_test = self.scale_y.transform(self.y_test)
        self.saveScalers()
        
    def reverseNormalization(self):
        self.x = self.scale_x.inverse_transform(self.x)
        self.y = self.scale_y.inverse_transform(self.y)
        self.x_test = self.scale_x.inverse_transform(self.x_test)
        self.y_test = self.scale_y.inverse_transform(self.y_test)
                                                
        if self.predictions is not None:
            self.predictions = self.scale_y.inverse_transform(self.predictions)
        
    def addInputLayer(self, inputs, neurons, activation, k_init="he_uniform"):
        self.model.add(Dense(neurons, input_dim=inputs, activation=activation, kernel_initializer=k_init))

    def addHiddenLayer(self, neurons, activation, k_init="he_uniform"):
        self.model.add(Dense(neurons, activation=activation, kernel_initializer=k_init))

    def addOutputLayer(self, outputs, activation='relu', bias_initializer='random_uniform'):
        self.model.add(Dense(outputs, activation=activation, bias_initializer=bias_initializer))

    def addConv2DLayer(self, filters, filter_size, input_shape, activation=None):
        self.model.add(Conv2D(filters, kernel_size=filter_size, input_shape=input_shape, activation=activation))
        
    def addFlatten(self):
        self.model.add(Flatten())
        
    def addCNNOutputLayer(self, outputs, activation='softmax'):
        self.model.add(Dense(outputs, activation=activation))

    def addConv1DInputLayer(self, filters, filter_size, input_size, activation='relu'):
        self.model.add(Conv1D(filters=filters, kernel_size=filter_size, 
                              activation=activation, input_shape=input_size))

    def addConv1DLayer(self, filters, filter_size, activation='relu'):
        self.model.add(Conv1D(filters=filters, kernel_size=filter_size, 
                              activation=activation))        

    def addDropout(self, density):
        self.model.add(Dropout(density))

    def addMaxPooling1D(self, pool_size):
        self.model.add(MaxPooling1D(pool_size))

    def addMaxPooling2D(self, pool_size=2):
        self.model.add(MaxPooling2D(pool_size=pool_size))
            
    def addGlobalAveragePooling1D(self):
        self.model.add(GlobalAveragePooling1D())
        
    def compileModel(self, loss, opt):
        if loss == "categorical_crossentropy":
            self.categorical = True
        self.model.compile(loss=loss, optimizer=opt)

    def fit(self, epochs, batch_size=0, verbose=0):
        if self.nn_type == "ANN":
            self.model.fit(self.x, self.y, epochs=epochs, batch_size=batch_size, verbose=verbose)
        elif self.nn_type.startswith("CNN"):
            if self.categorical:
                self.model.fit(self.x, to_categorical(self.y), epochs=epochs)
            else:
                self.model.fit(self.x, self.y, epochs=epochs)

    def saveScalers(self, filename='test'):
        joblib.dump(self.scale_x, filename + "_x_scaler.save")
        joblib.dump(self.scale_y, filename + "_y_scaler.save")
        
    def saveModel(self, filename="test"):
        self.model.save(filename + ".b5")
        self.saveScalers(filename)
       
    def loadModel(self, filename="test"):
        self.model = load_model(filename + ".b5")
        try:
            self.scale_x = joblib.load(filename + "_x_scaler.save")
            self.scale_y = joblib.load(filename + "_y_scaler.save")
        except FileNotFoundError:
            print ("Scaler files not found")
            self.scale_x = None
            self.scale_Y = None
        
    def fullPrediction(self):
        self.predictions = self.model.predict(self.x)

    def predict(self, val):
        if self.scale_x is not None:
            x = self.scale_x.transform(self.my_reshape(val))
        else:
            x = self.my_reshape(val)
            
        if self.scale_y is not None:
            r = self.scale_y.inverse_transform(self.model.predict(x))
        else:
            r = self.model.predict(x)
        return r
        
    def evaluate(self):
        eval1 = self.model.evaluate(self.x, self.y)
        print('Training: {}'.format(eval1))
    
        eval2 = self.model.evaluate(self.x_test, self.y_test)
        print('Test: {}'.format(eval2))
