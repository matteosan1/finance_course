import numpy as np

from scipy.stats import multivariate_normal, norm

class GaussianCopula:
    def __init__(self, n, cov):
        self.mv = multivariate_normal(mean=np.zeros(n), cov=cov)

    def sample(self, simulations):
        x = self.mv.rvs(size=simulations)
        return norm.cdf(x)