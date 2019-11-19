from keras.models import load_model
import pandas as pd
import matplotlib.pyplot as plt

model = load_model('bs_model.h5')

dataset = pd.read_csv("bs_testing.csv")
X_test = dataset.iloc[:, :4].values
Y_test = dataset.iloc[:, 4].values

plt.plot(model.predict(X_test), color="red", label="NN price")
plt.plot(Y_test, label="BS price")
plt.legend()
plt.show()
plt.savefig("comparison_fair.png")

dataset = pd.read_csv("bs_testing_off.csv")
X_test = dataset.iloc[:, :4].values
Y_test = dataset.iloc[:, 4].values

plt.plot(model.predict(X_test), color="red", label="NN price")
plt.plot(Y_test, label="BS price")
plt.legend()
plt.show()
plt.savefig("comparison_off.png")

