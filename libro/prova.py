from scipy.optimize import fsolve

def f(x):
    return -98.3 + 2.5/(1+0.0603/2) + 102.5/(1+x/2)**2

r = fsolve(f, .01)

print (r)
