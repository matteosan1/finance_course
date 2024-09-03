from scipy.optimize import brentq

def func(x):
    return 100 - 8/(1+0.04) - 8/(1+0.0503)**2 - 8/(1+0.0608)**3
               - 8/(1+0.0719)**4 - 108/(1+x)**5
               
a = brentq(func, 0, 0.10)
print (f"5y rate: {a:.4f}")