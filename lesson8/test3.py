import numpy as np, joblib
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from finnn import FinNN
from finmarkets import call


f = FinNN()

#x = np.array([[4,5,6]])
#x = x.reshape(3, 1)

#s = MinMaxScaler()
#x = s.fit_transform(x)

#print (x)

f.loadModel('test')
rv = np.array([[0.015, 0.234]])
#rv = rv.reshape(1, 2)
print ('{} => {} (expected {})'.format(rv.tolist(), 
                                       f.predict(rv), 
                                       call(1, rv[0][0], rv[0][1], 1)))
