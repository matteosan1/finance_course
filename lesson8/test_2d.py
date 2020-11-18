import numpy as np, json
import mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

#from PIL import Image

#vols = json.load(open("vols.json"))
#rates = json.load(open("rates.json"))
#
#train_labels = []
#for i in range(len(vols)):
#    for j in range(len(rates)):
#        train_labels.append((vols[i], rates[j]))
#
#image_pixels = []
#for i in range(10000):
#    original = Image.open('training_images/{}.png'.format(i))
#    width, height = original.size
#    pixels = []
#    for y in range(20):
#        l = []
#        for x in range(20):
#            pixel = original.getpixel((x, y))
#            l.append(pixel)
#        pixels.append(l)
#    image_pixels.append(pixels)
#
#json.dump(train_labels, open("2d_label.json", "w"))
#json.dump(image_pixels, open("2d.json", "w"))

images = np.array(json.load(open("2d.json")))
labels = np.array(json.load(open("2d_label.json")))

images = (images / 255) - 0.5
images = np.expand_dims(images, axis=3)

x_train, x_test, z_train, z_test = train_test_split(images, labels,
                                                    test_size=0.2)

num_filters = 8
filter_size = 3
pool_size = 2

model = Sequential()
model.add(Conv2D(num_filters, kernel_size=(20, 20),
                 input_shape=(20, 20, 1), activation='relu'))
model.add(Flatten())
model.add(Dense(10, activation='relu'))
model.add(Dense(2, activation='relu', bias_initializer='random_uniform'))
model.compile('adam', loss="mse")

model.fit(x_train, z_train, batch_size=32, epochs=300, verbose=1)
model.save("2d.b5")
eval1 = model.evaluate(x_train, z_train)
print('Training: {}'.format(eval1))

eval2 = model.evaluate(x_test, z_test)
print('Test: {}'.format(eval2))

