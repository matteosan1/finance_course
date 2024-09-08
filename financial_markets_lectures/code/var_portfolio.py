import numpy as np

w = np.array([0.1, 0.2, 0.5, 0.05, 0.1])
R = np.array([0.239188, 0.415127, 0.263797, 0.172818, 0.528046])
Sigma = np.array([[0.051902, 0.025037, 0.025737, 0.022454, 0.027760],
                  [0.025037, 0.085839, 0.041025, 0.039501, 0.048412],
                  [0.025737, 0.041025, 0.069550, 0.036127, 0.044528],
                  [0.022454, 0.039501, 0.036127, 0.051797, 0.040390],
                  [0.027760, 0.048412, 0.044528, 0.040390, 0.178298]])

ret = R.dot(w) # np.dot(R, w)
var = w.T.dot(Sigma.dot(w)) # np.dot(w.T, np.dot(Sigma, w))
std = np.sqrt(var)
print (f"Portfolio return {ret:.4f}")
print (f"Portfolio variance {var:.4f}")
print (f"Portfolio std. dev. {std:.4f}")
