import numpy as np
import json
from keras.models import Sequential, load_model
from keras.utils import to_categorical
from matplotlib import pyplot as plt

test_images = []

with open("testing_techana_frames.json", "r") as f:
    test_images = json.load(f)

test_images = np.array(test_images)
for i in range(test_images.shape[0]):
    plt.plot(test_images[i, :])
    plt.show()
test_images = np.expand_dims(test_images, axis=3)

model = load_model('techana.h5')

predictions = model.predict(test_images)
for i in range(len(predictions)):
    print (np.argmax(predictions[i]), max(predictions[i]))
    
