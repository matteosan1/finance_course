import numpy as np
from scipy.integrate import quad
	
def f(x, a):
    return np.exp(-x)/(a+(x-1)**2)
	
s = quad(f, 0, np.inf, args=(3,))
print (s)