from keras.models import Sequential
from keras.layers import Dense

model = Sequential()
model.add(Dense(15, input_dim=1, activation='sigmoid'))
model.add(Dense(5, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='mse', optimizer='adam')
model.fit(X_train, y_train, epochs=5000, batch_size=10, verbose=1)
