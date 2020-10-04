import argparse
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import SGD
#from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, train_test_split, KFold
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

X, Y, scale_x, scale_y = None, None, None, None

def init(filename):
    global X, Y, scale_x, scale_y
    
    dataset = pd.read_csv(filename)
    X = dataset.iloc[:, :4].values
    Y = dataset.iloc[:, 4].values

    X = X.reshape((len(X), 4))
    Y = Y.reshape((len(Y), 1))
    
    scale_x = MinMaxScaler()
    X = scale_x.fit_transform(X)
    scale_y = MinMaxScaler()
    Y = scale_y.fit_transform(Y)

def invertTransform(X, Y, yhat):
    global scale_x, scale_y

    # inverse transforms
    x_plot = scale_x.inverse_transform(X)
    y_plot = scale_y.inverse_transform(Y)
    yhat_plot = scale_y.inverse_transform(yhat)

    return x_plot, y_plot, yhat_plot
    
def training():
    global X, Y, scale_x, scale_y
    
    init("bs_training.csv")
    
    model = Sequential()
    model.add(Dense(50, input_dim=4, kernel_initializer='he_uniform', activation='sigmoid'))
    model.add(Dense(20, kernel_initializer='he_uniform', activation='sigmoid'))
    #model.add(Dense(50, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1))
        
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    
    model.fit(X, Y, epochs=500, verbose=1, batch_size=100)
    
    yhat = model.predict(X)
    
    x_plot, y_plot, yhat_plot = invertTransform(X, Y, yhat)
    
    print('MSE: {:.3f}'.format(mean_squared_error(y_plot, yhat_plot)))
    plt.scatter(range(0, len(y_plot)), (y_plot - yhat_plot)/y_plot, label='Actual')
    plt.show()

#    kfold = KFold(n_splits=2, shuffle=True, random_state=7)
#    scores = []
#    for train, test in kfold.split(X, Y):
#        # create model
#        model = Sequential()
#        model.add(Dense(10, input_dim=1, kernel_initializer='normal', activation='relu'))
#        model.add(Dense(4, kernel_initializer='normal', activation='relu'))
#        #model.add(Dense(50, kernel_initializer='normal', activation='relu'))
#        model.add(Dense(1, kernel_initializer='normal'))
#        
#        model.compile(loss='mse', optimizer='adam', metrics=['mae'])
#    
#        history = model.fit(X[train], Y[train], epochs=50, verbose=1, batch_size=25)
#        s = model.evaluate(X[test], Y[test])
#        print("{}: {:2f}".format(model.metrics_names[1], s[1]))
#        scores.append(s[1])
#
#    print (np.mean(scores), np.std(scores))
    model.save('bs_model.h5')


def testing():
    global X, Y, scale_x, scale_y
    
    model = load_model('bs_model.h5')
    init("bs_testing.csv")
    
    predictions = model.predict(X)
    
    x_plot, y_plot, predictions = invertTransform(X, Y, predictions)

    for i in range(0, 5):
        print ('{} => {} (expected {})'.format(x_plot[i].tolist(), predictions[i], y_plot[i]))
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Black-Scholes NN training')
    parser.add_argument('-t', '--training', action='store_true', dest="training", default=False, help='run training routine')
    parser.add_argument('-T', '--testing', action='store_true', dest="testing", default=False, help='run testing routine')
    parser.add_argument('-a', '--all', action='store_true', dest="all", default=False, help='run training and testing routines')
    
    args = vars(parser.parse_args())

    if args['training']:
        training()
    elif args['testing']:
        testing()
    elif args['all']:
        training()
        testing()
