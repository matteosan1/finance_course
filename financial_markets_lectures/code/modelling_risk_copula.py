import numpy as np, pandas as pd

from scipy.stats import multivariate_normal, norm
from typing import Dict, List, Tuple, Union

class Copula:
    def __init__(self, n: int, typ: str, params: dict):
        self.n = n
        self.type = typ.lower()
        self.mean = np.zeros(n)
        self.corr = params.get('corr')
        
        self._normalize_cov()

        if self.type == "gauss":
            self.mv = multivariate_normal(mean=self.mean, cov=self.corr)
        else:
            raise ValueError(f"Copula type {type} unknown.")
        self.x = None
        self.samples = None

    def _normalize_cov(self):
        self.corr = 2*np.sin(np.pi/6*self.corr)
        std_devs = np.sqrt(np.diag(self.corr))
        outer_std = np.outer(std_devs, std_devs)
        self.corr = self.corr/outer_std

    def rvs(self, size: int, seed: int=1):        
        np.random.seed(seed)
        self.x = self.mv.rvs(size=size)
        if self.type == "gauss":
            self.samples = norm.cdf(self.x)
        else:
            raise ValueError(f"Copula type {type} unknown. "
                             "Available types: gauss, t")
    
    def rvs_marginals(self, distributions) -> np.array:
        if len(distributions) != self.n:
            raise ValueError(f"Expected {self.n} distributions, "
                             "got {len(distributions)}")
        if self.samples is None:
            raise ValueError(f"Please first sample from copula with rvs.")

        correlated_samples = np.zeros_like(self.samples)
        for i, dist in enumerate(distributions):
            if hasattr(dist, "ppf"):
                correlated_samples[:, i] = dist.ppf(self.samples[:, i])
            else:
                raise TypeError(f"Element at index {i} must have "
                                "a .ppf() method.")
        return correlated_samples
