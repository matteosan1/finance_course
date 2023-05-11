import numpy as np, mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.utils import to_categorical

train_images = mnist.train_images()
train_labels = mnist.train_labels()

model = Sequential()



model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)))
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(512, activation="relu", name="dense1"))
model.add(Dense(10, activation="softmax", name='dense2'))

#model.add(Conv2D(8, kernel_size=3, input_shape=(28, 28, 1)))
#model.add(MaxPooling2D(pool_size=2))
#model.add(Flatten())
#model.add(Dense(10, activation="softmax"))
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.fit(train_images, to_categorical(train_labels), epochs=5, verbose=1)
model.save("test")
