from scipy.stats import multivariate_normal
import numpy as np

np.random.seed(10)

trials = 1000
m_norm = multivariate_normal(mean=[0, 0], cov=[[1,0],
                                               [0,1]])

X = m_norm.rvs(size=trials)

sigma = np.array([[3, 1], [1, 1]])
L = np.linalg.cholesky(sigma)
Z = X.dot(L)
print (L)