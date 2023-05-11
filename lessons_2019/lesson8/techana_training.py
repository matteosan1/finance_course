import numpy as np
import json
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv1D, Dropout, Flatten, MaxPooling1D
from keras.utils import to_categorical

# load the training set
with open("training_techana_labels.json", "r") as f:
    train_labels = json.load(f)
#train_labels = train_labels[:]
train_images = []

with open("training_techana_images.json", "r") as f:
    train_images = json.load(f)
#train_images = train_images[:]
train_images = np.array(train_images)
train_images = np.expand_dims(train_images, axis=3)

# define the CNN 
model = Sequential()
model.add(Conv1D(filters=80, kernel_size=20, activation='relu', input_shape=(101, 1)))
model.add(Conv1D(filters=80, kernel_size=15, activation='relu'))
model.add(MaxPooling1D(3))
model.add(Conv1D(filters=100, kernel_size=10, activation='relu'))
model.add(Conv1D(filters=100, kernel_size=5, activation='relu'))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(3, activation="softmax"))

model.compile(loss='categorical_crossentropy', 
              optimizer='adam', metrics=['accuracy'])

# make the training
model.fit(train_images, to_categorical(train_labels), 
          epochs=150, batch_size=35, verbose=2)

model.save('techana.h5')
