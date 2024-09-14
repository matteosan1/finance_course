import numpy as np, matplotlib.pyplot as plt

from finmarkets.ml.network import Network
from finmarkets.ml.fc_layer import FCLayer
from finmarkets.ml.activation_layer import ActivationLayer
from finmarkets.ml.activations import tanh, tanh_prime
from finmarkets.ml.losses import mse, mse_prime

from keras.datasets import mnist

def one_hot(Y):
    one_hot_Y = np.zeros((Y.size, 10))
    one_hot_Y[np.arange(Y.size), Y] = 1
    return one_hot_Y

(X_train, Y_train), (X_test, Y_test) = mnist.load_data()

X_train = X_train.reshape(X_train.shape[0], 1, 28*28)
X_train = X_train.astype('float32')
X_train /= 255
Y_train = one_hot(Y_train)

X_test = X_test.reshape(X_test.shape[0], 1, 28*28)
X_test = X_test.astype('float32')
X_test /= 255
y_test = one_hot(Y_test)

net = Network()
net.add(FCLayer(28*28, 100))
net.add(ActivationLayer(tanh, tanh_prime))
net.add(FCLayer(100, 50))
net.add(ActivationLayer(tanh, tanh_prime))
net.add(FCLayer(50, 10))
net.add(ActivationLayer(tanh, tanh_prime))

net.use(mse, mse_prime)
net.fit(X_train[0:1000], Y_train[0:1000], epochs=35, learning_rate=0.1)

for i in range(3):
  current_image = X_test[i].reshape((28, 28)) * 255
  plt.gray()
  plt.imshow(current_image, interpolation='nearest')
  plt.show()
  out = net.predict(X_test[i])[0]
  idx = np.argmax(out[0])
  print(f"predicted value: {idx} (prob. {out[0][idx]:.3f})")
  print(f"true value: {Y_test[i]}")
