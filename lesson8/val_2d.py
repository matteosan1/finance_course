from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from keras.models import load_model
import numpy as np
import json
import random

random.seed(1)
items = [random.randint(0, 10000) for _ in range(10)]
labels = np.array( json.load(open("2d_label.json")))
model = load_model("2d.b5")
images = np.array(json.load(open("2d.json")))
images = (images / 255) - 0.5
images = np.expand_dims(images, axis=3)

for item in items:
    image = images[item]
    image = np.array(np.array([image]))
    pred = model.predict(image)
    dist = np.sqrt((pred[0][0]-labels[item, 0])**2 +
                   (pred[0][1]-labels[item, 1])**2)
    print ("Prediction: {} <=> Truth: {} (dist. {:.3f})".format(pred[0],
                                                            labels[item],
                                                            dist))

