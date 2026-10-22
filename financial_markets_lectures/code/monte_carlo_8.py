import numpy as np
from scipy.stats import norm

samples = [1.,2.,3.,4.,4.,4.,5.,5.,5.,5.,4.,4.,4.,6.,7.,8.]
alpha = 0.95
X = np.array(samples)
A = norm.ppf((1 + alpha)/2)
m, se = np.mean(X), np.std(X)
h = A*se/np.sqrt(len(samples))
print (f"{alpha*100:.0f}% confidence int.: {m:.3f} +- {h:.3f}")