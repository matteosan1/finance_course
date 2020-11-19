# example of fitting a neural net on x vs x^2
from sklearn.preprocessing import MinMaxScaler
#from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from numpy import asarray, arange
from matplotlib import pyplot as plt

import pandas as pd
import numpy as np
from finmarkets import call

state = 3
bins = 800

if state == 1:
    import csv

    z = []
    vols = np.arange(0.15, 0.55, (0.55-0.15)/bins)
    rates = np.arange(0., 0.1, (.1-.0)/bins)

    with open("test.csv", "w") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i1 in range(bins):
            for i2 in range(bins):
                z.append(call(1, rates[i1], vols[i2], 1))
                writer.writerow([vols[i2], rates[i1], z[-1]])                

elif state == 2:
    from keras.models import Sequential
    from keras.layers import Dense, Dropout

    dataset = pd.read_csv("test.csv")

    x = dataset.iloc[:, 1:3].values
    z = dataset.iloc[:, 0].values
    print (z.shape)
    z = z.reshape((len(z), 1))
    print (z.shape)
    scale_x = MinMaxScaler()
    x = scale_x.fit_transform(x)
    scale_z = MinMaxScaler()
    z = scale_z.fit_transform(z)
    
    x_train, x_test, z_train, z_test = train_test_split(x, z, test_size=0.33)
    model = Sequential()
    model.add(Dense(20, input_dim=2, kernel_initializer='he_uniform', activation='sigmoid'))
    #model.add(Dropout(0.2))
    model.add(Dense(8, kernel_initializer='he_uniform', activation='sigmoid'))
    #model.add(Dropout(0.2))
    model.add(Dense(1))
    
    model.compile(loss='mse', optimizer='adam')
    
    model.fit(x_train, z_train, epochs=200, verbose=1, batch_size=1500)

    model.save("test_inv.b5")
    
    eval1 = model.evaluate(x_train, z_train)
    print('Training: {}'.format(eval1))
    
    eval2 = model.evaluate(x_test, z_test)
    print('Test: {}'.format(eval2))
    
elif state == 3:
    from keras.models import load_model

    model = load_model("test_inv.b5")
    dataset = pd.read_csv("test.csv")

#    vols = dataset.iloc[:, 0].values
#    rates = dataset.iloc[:, 2].values

    x = dataset.iloc[:, 1:3].values
    z = dataset.iloc[:, 0].values
    
    x = x.reshape((len(x), 2))
    z = z.reshape((len(z), 1))
    
    scale_x = MinMaxScaler()
    x = scale_x.fit_transform(x)
    scale_z = MinMaxScaler()
    z = scale_z.fit_transform(z)

    
    
    predictions = model.predict(x)
    #zt = z[:]*0.4+0.15
    zt = scale_z.inverse_transform(z)
    zhat = scale_z.inverse_transform(predictions)
    #print (zt[:10, 0])
    #print (zhat[:10])
           
    #for i in range(100):
    #    print (z[i], zhat[i])

#    from mpl_toolkits import mplot3d
    
#    fig = plt.figure()
#    ax = plt.axes(projection='3d')
    
#    vols = vols.reshape(bins, bins)
#    rates = rates.reshape(bins, bins)
    #rates = rates.copy().T
#    z = z.reshape(bins, bins)
#    zhat = zhat.reshape(bins, bins)

    res = (zt-zhat)/zt
    from matplotlib import pyplot as plt
    plt.plot(res)
    plt.show()
    
#    ax.plot_surface(vols, rates, res, cmap='viridis', edgecolor='grey')
#    ax.set_xlabel("volatility")
#    ax.set_ylabel("rate")
#    ax.set_zlabel("m.s.e.")
#    #ax.set_zlim3d(-.01, .01)
#    #ax.set_xlim3d(.25, .55)
#    plt.show()
#
