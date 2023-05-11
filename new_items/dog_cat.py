import os
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.utils import to_categorical

from sklearn.model_selection import train_test_split

path = "train/"
filenames = os.listdir(path)

#labels = []
#imgs = []
#for i, f in enumerate(filenames):
#    if i%2 == 0:
#        continue
#    if f.split('.')[0] == 'cat':
#        labels.append(0) # cat
#    else:
#        labels.append(1) # dog
#        
#    im = np.array(load_img(path + f, target_size=(100, 100)))
#    im = np.mean(im, axis=2)/255.
#    im = im.reshape(10000)
#    imgs.append(im)
#    if i % 1001 == 0:
#        print (len(imgs))
#
#imgs = np.array(imgs)
#labels = np.array(labels)
#
#with open('images.npy', 'wb') as f:
#    np.save(f, imgs)
#with open('labels.npy', 'wb') as f:
#    np.save(f, labels)
#quit()

with open('images.npy', 'rb') as f:
    imgs = np.load(f)

with open('labels.npy', 'rb') as f:
    labels = np.load(f)

X_train, X_test, y_train, y_test = train_test_split(imgs, labels, test_size=0.2, random_state=17)


#model = Sequential()
#model.add(Dense(5000, input_dim=10000, activation='relu'))
##model.add(Dense(5000, activation='relu'))
##model.add(Dense(1000, activation='relu'))
#model.add(Dense(500, activation='relu'))
#model.add(Dense(50, activation='relu'))
#model.add(Dense(1, activation='softmax'))
#
#model.compile(loss='binary_crossentropy', optimizer='adam')
#
#model.fit(X_train, y_train, #to_categorical(y_train),
#          batch_size=100, epochs=3, verbose=1)
#model.save("dog_cat.model")

model = load_model("dog_cat.model")

print (model.predict(X_train[:10]))
print (y_train[:10])

