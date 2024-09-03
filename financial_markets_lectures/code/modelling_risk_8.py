import numpy as np
from scipy.stats import chi2, t, multivariate_normal

n_samples = 1000000
nu = 2

sigma = np.array([[1, 0.1],[0.1, 1]])
L = np.linalg.cholesky(sigma)
mv = multivariate_normal(mean=[0, 0], cov=[[1, 0], [0, 1]])
Y = mv.rvs(size=n_samples)
Z = Y.dot(L)
S = chi2(nu).rvs(size=n_samples)
Z[:, 0] = np.sqrt(nu/S)*Z[:, 0]
Z[:, 1] = np.sqrt(nu/S)*Z[:, 1]

U = t(nu).cdf(Z)