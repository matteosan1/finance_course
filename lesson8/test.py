# example of fitting a neural net on x vs x^2
from sklearn.preprocessing import MinMaxScaler
#from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from numpy import asarray, arange
from matplotlib import pyplot as plt

from PIL import Image
import pandas as pd
import numpy as np
from finmarkets import call
import csv

state = 1
bins = 100

#def convert():
#    old_range = (old_max - old_min)
#    new_range = (new_max - new_min)
#    return (((OldValue - old_min)*new_range/old_range + new_min
#
if state == 1:
    print ("Generating outputs")
    z = []
    vols = np.arange(0.15, 0.55, (0.55-0.15)/bins)
    rates = np.arange(0., 0.1, (.1-.0)/bins)
    k = np.arange(0.8, 1.2, (1.2-0.8)/20)
    ttm = np.arange(1, 5, 4/20)

    import json
    print ("Saving outputs")
    json.dump(rates.tolist(), open("rates.json", "w"))
    json.dump(vols.tolist(), open("vols.json", "w"))

    print ("Generating inputs")
    maximum = 0
    minimum = np.inf
    prices = []
    index = 0
    for v in vols:
        for r in rates:
            if index %1000 == 0:
                print (index)
            price =  np.zeros(shape=(20, 20))
            for ik, kv in enumerate(k):
                for it, t in enumerate(ttm):
                    #print (kv, r, v, t)
                    price[ik, it] = call(kv, r, v, t)
            prices.append(price)
            new_max = np.max(price)
            new_min = np.min(price)
            if new_max > maximum:
                maximum = new_max
            if new_min < minimum:
                minimum = new_min
            index += 1
            
    print ("normalizing")
    for ip, p in enumerate(prices):
        prices[ip] = np.interp(p, (minimum, maximum), (0, 255)) 

    print ("Images")
    index = 0
    for v in vols:
        for r in rates:
            if index %1000 == 0:
                print (index)
            img = Image.new("L", (20, 20), color='black')
            for ik, kv in enumerate(k):
                for it, t in enumerate(ttm):
                    img.putpixel((ik, it), int(prices[index][ik, it]))
            img.save("training_images/{}.png".format(index)) 
            index += 1
#elif state == 2:
#    from keras.models import Sequential
#    from keras.layers import Dense, Dropout
#
#    dataset = pd.read_csv("test.csv")
#
#    x = dataset.iloc[:, :2].values
#    z = dataset.iloc[:, 2].values
#    print (z.shape)
#    z = z.reshape((len(z), 1))
#    print (z.shape)
#    scale_x = MinMaxScaler()
#    x = scale_x.fit_transform(x)
#    scale_z = MinMaxScaler()
#    z = scale_z.fit_transform(z)
#    
#    x_train, x_test, z_train, z_test = train_test_split(x, z, test_size=0.33)
#    #import sys
#    #sys.exit()
#    model = Sequential()
#    model.add(Dense(20, input_dim=2, kernel_initializer='he_uniform', activation='sigmoid'))
#    #model.add(Dropout(0.2))
#    model.add(Dense(8, kernel_initializer='he_uniform', activation='sigmoid'))
#    #model.add(Dropout(0.2))
#    model.add(Dense(1))
#    
#    model.compile(loss='mse', optimizer='adam')
#    
#    model.fit(x_train, z_train, epochs=5000, verbose=1, batch_size=500)
#
#    model.save("test.b5")
#    
#    eval1 = model.evaluate(x_train, z_train)
#    print('Training: {}'.format(eval1))
#    
#    eval2 = model.evaluate(x_test, z_test)
#    print('Test: {}'.format(eval2))

elif state == 3:
    from keras.models import load_model

    model = load_model("test.b5")
    dataset = pd.read_csv("test.csv")

    vols = dataset.iloc[:, 0].values
    rates = dataset.iloc[:, 1].values

    x = dataset.iloc[:, :2].values
    z = dataset.iloc[:, 2].values
    
    x = x.reshape((len(x), 2))
    z = z.reshape((len(z), 1))
    
    scale_x = MinMaxScaler()
    x = scale_x.fit_transform(x)
    scale_z = MinMaxScaler()
    z = scale_z.fit_transform(z)

    predictions = model.predict(x)
    z = scale_z.inverse_transform(z)
    zhat = scale_z.inverse_transform(predictions)
    #for i in range(100):
    #    print (z[i], zhat[i])

    from mpl_toolkits import mplot3d
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    vols = vols.reshape(bins, bins)
    rates = rates.reshape(bins, bins)
    #rates = rates.copy().T
    z = z.reshape(bins, bins)
    zhat = zhat.reshape(bins, bins)

    res = (z-zhat)/z
    
    ax.plot_surface(vols, rates, res, cmap='viridis', edgecolor='grey')
    ax.set_xlabel("volatility")
    ax.set_ylabel("rate")
    ax.set_zlabel("m.s.e.")
    #ax.set_zlim3d(-.01, .01)
    #ax.set_xlim3d(.25, .55)
    plt.show()

