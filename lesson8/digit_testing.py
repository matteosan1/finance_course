import numpy as np
import mnist
from keras.models import load_model

model = load_model('digit_training.h5')

# testing with mnist test sample
test_images = mnist.test_images()
test_labels = mnist.test_labels()

test_images = (test_images / 255) - 0.5
test_images = np.expand_dims(test_images, axis=3)

predictions = model.predict(test_images[:5])
print ("Tesing on MNIST digits...")
print("Predicted: ", np.argmax(predictions, axis=1)) # [7, 2, 1, 0, 4]
print("Truth:", test_labels[:5])
print("%:", ["{:.3f}".format(p[np.argmax(p)]) for p in predictions]) # [7, 2, 1, 0, 4]

# testing with custom digits
from digit_converter import transform_images

test_images = transform_images()

test_images = np.array(test_images)
test_images = (test_images / 255) - 0.5
test_images = np.expand_dims(test_images, axis=3)

predict = model.predict(test_images)
print ("\n")
print ("Tesing on custom digits...")
print ("Predicted: ", np.argmax(predict, axis=1))
print ("Truth: [1 2 3 4 5 6 7 8 9 0 g]")
print(np.argmax(predict, axis=1))
print("%:", ["{:.3f}".format(p[np.argmax(p)]) for p in predict])
for i in [5, 6, 8, 10]:
    print("full ranking for {}:".format(i+1), ["{:.3f}".format(p) for p in predict[i]])