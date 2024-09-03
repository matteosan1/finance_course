import numpy as np

from scipy.optimize import brentq

C = np.array([[104, 0, 0, 0, 0],
              [5, 105, 0, 0, 0],
              [6, 6, 106, 0, 0],
              [7, 7, 7, 107, 0],
              [8, 8, 8, 8, 108]])
P = np.array([100, 100, 100, 100, 100])

Cinv = np.linalg.inv(C)
d = Cinv.dot(P.T)
print (d)

def rate(x, d, tau):
    return d - 1/(1+x)**tau

for i in range(5):
    print (f"yield y{i+1}: {brentq(rate, 0, 1, args=(d[i], i+1)):.4f}")
