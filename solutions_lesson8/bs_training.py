from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import SGD
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score, train_test_split, KFold
from sklearn.metrics import accuracy_score
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("bs_training.csv")
X_train = dataset.iloc[:, :4].values
Y_train = dataset.iloc[:, 4].values

# create model
model = Sequential()
model.add(Dense(10, input_dim=4, kernel_initializer='normal', activation='relu'))
#model.add(Dense(10, kernel_initializer='normal', activation='relu'))
model.add(Dense(1, kernel_initializer='normal'))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse', 'mae'])

history = model.fit(X_train, Y_train, epochs=1000, verbose=1, batch_size=100)
evaluator = model.evaluate(X_train, Y_train)
print('Test: {}'.format(evaluator))

model.save('bs_model.h5')


model = load_model('bs_model.h5')

#dataset = pd.read_csv("bs_training.csv")
#X_test = dataset.iloc[:, :4].values
#Y_test = dataset.iloc[:, 4].values
#
#plt.plot(model.predict(X_test), color="red", label="NN price")
#plt.plot(Y_test, label="BS price")
#plt.legend()
#plt.show()
#plt.savefig("comparison_fair.png")
##predictions = model.predict(X_test)
##for i in range(5):
##    print ('{} => {} (expected {})'.format(X_test[i].tolist(), predictions[i], Y_test[i]))

