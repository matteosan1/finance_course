from numpy import pi
from scipy.optimize import minimize

def obj_func(x):
    return 2*330/x[0] + 2*pi*x[0]**2

x0 = [1]
bounds = [(0.01, 100)]

r = minimize(obj_func, x0, bounds=bounds)
print (r)
