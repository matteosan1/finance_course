import numpy as np, mnist

from keras.models import Sequential, load_model
from keras.layers import Dense
from tensorflow.keras.utils import to_categorical

train_images = mnist.train_images()
train_images = train_images.reshape(60000, 784)
train_images = train_images/(255/2) - 1
train_labels = mnist.train_labels()
      
model = Sequential()
model.add(Dense(300, input_dim=784, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

model.fit(train_images, to_categorical(train_labels),
          batch_size=500, epochs=400, verbose=1)
model.save("digits.model")
