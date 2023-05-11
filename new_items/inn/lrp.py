import numpy as np, pandas as pd, joblib

from scipy.stats import norm

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential, load_model, Model
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
import sys
sys.setrecursionlimit(100)

def d1(S_t, K, r, vol, ttm):
  num = np.log(S_t/K) + (r + 0.5*np.power(vol, 2)) * ttm
  den = vol * np.sqrt(ttm)
  return num/den

def d2(S_t, K, r, vol, ttm):
  return d1(S_t, K, r, vol, ttm) - vol * np.sqrt(ttm)

def call(S_t, K, r, vol, ttm):
  return S_t * norm.cdf(d1(S_t, K, r, vol, ttm)) - K * np.exp(-r * ttm) * norm.cdf(d2(S_t, K, r, vol, ttm))

def put(S_t, K, r, vol, ttm):
  return K * np.exp(-r * ttm) * norm.cdf(-d2(S_t, K, r, vol, ttm)) - S_t * norm.cdf(-d1(S_t, K, r, vol, ttm))

def func():
    x = np.arange(-3, 3, 0.1)
    y = np.power(x, 3) + 2
    return x, y
    
#def part1():
strike_range = np.arange(20, 40.1, 0.1)
sigma_range = np.arange(0.10, 0.601, 0.001)
r = 0.0011
S0 = 30.93
ttm = 1

#d = {"K":[], "vol":[], "price":[]}
#
#for K in strike_range:
#    for sigma in sigma_range:
#        d["K"].append(K)
#        d["vol"].append(sigma)
#        d['price'].append(call(S0, K, r, sigma, ttm))
#
#df_c = pd.DataFrame(d)
#df_c.to_csv("dataset.csv")
#quit()
#df_c= pd.read_csv("dataset.csv")
#x = df_c[['K', 'price']]
#y = df_c[['vol']]
#x_scale_c = MinMaxScaler()
#y_scale_c = MinMaxScaler()
#x_train = x_scale_c.fit_transform(x)
#y_train = y_scale_c.fit_transform(y)
#
model = Sequential()
model.add(Dense(20, input_dim=2, activation=None))
#model.add(Dense(8, activation='relu'))
#model.add(Dense(5, activation='relu'))
model.add(Dense(1, activation=None))
model.compile(loss='mse', optimizer='adam')
#earlyStop = EarlyStopping(monitor='loss', mode='min', patience=50)
#model.fit(x_train, y_train, epochs=2, batch_size=100, verbose=1)#, callbacks=[earlyStop])
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.models import Sequential

model = Sequential()
model.add(Conv2D(64,(3, 3), activation='relu', input_shape=(150, 150, 3), data_format="channels_last"))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(128,(3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(256,(3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(256,(3, 3), activation='relu'))
model.add(MaxPooling2D((2,2)))

model.add(Flatten())
model.add(Dense(512, activation='relu', name='dense1'))
model.add(Dense(2, activation='softmax', name='dense2'))

model.compile(loss='categorical_crossentropy', optimizer="adam")
#X, y = func()
#
#  scaleX = MinMaxScaler()
#  scaley = MinMaxScaler()
#  
#  X_train = scaleX.fit_transform(X.reshape(-1, 1))
#  y_train = scaley.fit_transform(y.reshape(-1, 1))
#joblib.dump(x_scale_c, "function_approx_X_scaler.save")
#joblib.dump(y_scale_c, "function_approx_y_scaler.save")

#  model = Sequential()
#  model.add(Dense(10, input_dim=1, activation='relu'))
#  model.add(Dense(5, activation='relu'))
#  model.add(Dense(1, activation='relu'))
#  
#  model.compile(loss='mse', optimizer='adam')
#  model.fit(X_train, y_train, epochs=5000, batch_size=50, verbose=1)
#model.save("bs2")

#part1()

#model = load_model("bs2")
#scaleX = joblib.load("function_approx_X_scaler.save")
#scaley = joblib.load("function_approx_y_scaler.save")

x0 = np.array([[30.0, 4.132]])
#x0 = x_scale_c.transform(x0)
#print (x0)
#y0 = model.predict(x0)
#print (scaley.inverse_transform(y0))
#quit()


class LRP:
    """
    LRP - utility class to perform Layerwise Relevance Propagation. Currently it works only on dense layers.

    Params:
    -------
    model: tensorflow.keras.models.Model
        The Keras trained model to work with.
    epsilon: float
        Normalization factor for LRP step 2 calculation.
    """
    def __init__(self, model, epsilon=1e-9):
        self.model = model
        self.names, self.activations, self.weights, self.biases = [], [], [], []
        for layer in model.layers:
            self.names.append(layer.name)
            self.activations.append(Model(inputs=model.input, outputs=layer.output))
            w = layer.get_weights()
            self.weights.append(w[0])
            self.biases.append(w[1])
        self.nlayers = len(self.names)
        self.epsilon = epsilon

    def summary(self):
        """
        summary - shows a model summary with numerical details on the weights.

        Params:
        -------
        None
        """
        print ("nlayers: ", self.nlayers)
        print ("+++++++++++")
        for l in range(self.nlayers):
            print ("Layer name: {}".format(self.names[l]))
            print ("Weights:\n", self.weights[l])
            print ("Bias:\n", self.biases[l])
            print ("------------")

    def rho(self, w, l, types):
        if types[l][0] == 'gamma':
            return w + np.maximum(0, w) * types[l][1]
        else:
            return w

    def incr(self, z, l, types):
        z += self.epsilon
        if types[l][0] == 'epsilon':
            return z + (z**2).mean()**0.5 * types[l][1]
        else:
            return z
            
    def lrp(self, X, types):
        """
        lrp - performes the actual relevance propagation and output the input relevance matrix.
        
        Params:
        -------
        X: numpy.array
            The specific input on which we want to compute the relevance.
        types: list(tuple)
            List of tuples with LRP rule types: (type, param). Possible types are: zero, epsilon and gamma; 
            parameters are the gamma or the epsilon values.
        """
        y = self.model.predict(X)
        print ("LRP for input:\n", X)
        A = [np.array([X])] + [None]*self.nlayers
        for l in range(self.nlayers):
            A[l+1] = np.maximum(0, A[l].dot(self.weights[l]) + self.biases[l])
            #A[l+1] = self.activations[l].predict(X)

        R = [None]*self.nlayers + [A[self.nlayers]*y]
        for l in range(self.nlayers-1, 0, -1):
            w = self.rho(self.weights[l], l, types)
            b = self.rho(self.biases[l], l, types)

            z = self.incr(A[l].dot(w) + b, l, types)
            s = R[l+1]/z
            c = s.dot(w.T)
            R[l] = A[l]*c

        w = self.weights[0]
        wm, wp = np.minimum(0, w), np.maximum(0, w)
        lb = A[0]*0-1
        hb = A[0]*0+1
        z = A[0].dot(w) - lb.dot(wp) - hb.dot(wm)
        s = R[1]/z
        c, cp, cm = s.dot(w.T), s.dot(wp.T), s.dot(wm.T)
        R[0] = A[0]*c - lb*cp - hb*cm

        print ("Relevance:\n", R[0])
        return R

#lrp = LRP(model)
##lrp.summary()
#types = [None, # input layer
#         ("gamma", 0.1),
#         ("epsilon", 0.1),
#         ("zero", 0)] # output layer
#
#R = lrp.lrp(x0, types)

import innvestigate
import tensorflow as tf

model = load_model("bs2")
tf.compat.v1.disable_eager_execution()
analyzer = innvestigate.create_analyzer("guided_backprop", model)#, **{"epsilon":0.00000001})

analysis = analyzer.analyze(np.array([x0]))
print (analysis)
