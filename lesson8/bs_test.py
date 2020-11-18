from finnn import FinNN
import numpy as np
import pandas as pd
from finmarkets import call
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import load_model
from numpy import array, arange
from matplotlib import pyplot as plt

data =  pd.read_csv("bs_training_sample.csv")

x = data.iloc[:10000, 1:3].values
y = data.iloc[:10000, 0].values

y = y.reshape((len(y), 1))
scale_x = MinMaxScaler()
x = scale_x.fit_transform(x)
scale_y = MinMaxScaler()
y = scale_y.fit_transform(y)
    
x_train, x_test, z_train, z_test = train_test_split(x, y, test_size=0.33)

model = Sequential()
model.add(Dense(20, input_dim=2, kernel_initializer='he_uniform', activation='sigmoid'))
#model.add(Dropout(0.2))
model.add(Dense(8, kernel_initializer='he_uniform', activation='sigmoid'))
#model.add(Dropout(0.2))
model.add(Dense(1))

model.compile(loss='mse', optimizer='adam')

model.fit(x_train, z_train, epochs=5000, verbose=1, batch_size=250)

model.save("test2.b5")

eval1 = model.evaluate(x_train, z_train)
print('Training: {}'.format(eval1))

eval2 = model.evaluate(x_test, z_test)
print('Test: {}'.format(eval2))

#model = load_model('test2.b5')
x_new = model.predict(x_test)

x_new = (scale_y.inverse_transform(x_new))
z_test = (scale_y.inverse_transform(z_test))

print (z_test[2000:2010])
print (x_new[2000:2010])
from matplotlib import pyplot as plt
plt.plot((x_new-z_test)/z_test)
plt.show()
#trainer.loadModel('test_no_normalize')
#r = np.array([[0.000125, 0.15]])

#print (trainer.predict(r))
#print (call(1, r[0][0], r[0][1], 1))
#Using TensorFlow backend.
#2020-11-17 16:51:29.817592: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
#2020-11-17 16:51:29.821334: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 3200000000 Hz
#2020-11-17 16:51:29.821525: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x55fe51895fc0 executing computations on platform Host. Devices:
#2020-11-17 16:51:29.821557: I tensorflow/compiler/xla/service/service.cc:175]   StreamExecutor device (0): Host, Default Version
#Epoch 1/1000
#512640/512640 [==============================] - 2s 3us/step - loss: 0.0887
#Epoch 2/1000
#512640/512640 [==============================] - 1s 3us/step - loss: 0.0836
#Epoch 3/1000
#512640/512640 [==============================] - 1s 3us/step - loss: 0.0837
#Epoch 4/1000
#512640/512640 [==============================] - 2s 3us/step - loss: 0.0837
#Epoch 5/1000

#512640/512640 [==============================] - 1s 3us/step - loss: 4.8378e-04
#Epoch 996/1000
#512640/512640 [==============================] - 1s 3us/step - loss: 3.6750e-04
#Epoch 997/1000
#512640/512640 [==============================] - 2s 3us/step - loss: 4.6891e-04
#Epoch 998/1000
#512640/512640 [==============================] - 1s 3us/step - loss: 3.7741e-04
#Epoch 999/1000
#512640/512640 [==============================] - 1s 3us/step - loss: 4.4239e-04
#Epoch 1000/1000
#512640/512640 [==============================] - 1s 3us/step - loss: 4.2784e-04
#512640/512640 [==============================] - 8s 16us/step
#Training: 0.00038490771084832614
#128160/128160 [==============================] - 2s 16us/step
#Test: 0.00038465018545919227
