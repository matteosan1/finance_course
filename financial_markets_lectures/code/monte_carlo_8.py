import numpy as np

from numpy.random import random

def myrand(llim, ulim, n):
    return random(size=n)*(ulim-llim) + llim

def f(x, a):
    return np.exp(-x)/(a+(x-1)**2)

def integration_mc(f, args, llim, ulim, iter=10000):
    vals = f(myrand(llim, ulim, iter), *args)
    return (ulim-llim)*np.mean(vals)

print (integration_mc(f, (3,), 0, 5, 1000000))