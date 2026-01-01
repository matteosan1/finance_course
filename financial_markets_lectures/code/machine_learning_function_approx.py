from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input

model = Sequential()
model.add(Input(shape=(1,)))
model.add(Dense(15, activation='tanh'))
model.add(Dense(5, activation='tanh'))
model.add(Dense(1, activation=None))
model.compile(loss='mse', optimizer='adam')

history = model.fit(scaled_X, scaled_y, epochs=100, batch_size=10, verbose=1)
