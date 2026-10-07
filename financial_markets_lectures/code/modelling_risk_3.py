import numpy as np, pandas as pd, scipy

from scipy.stats import multivariate_normal, norm
from typing import Dict, List, Tuple, Union

class Copula:
  def __init__(self, n: int, typ: str, params: dict):
    self.n = n
    self.type = typ
    self.mean = params.get('mean', np.zeros(n))
    self.corr = params.get('corr')        
    self.df = params.get('df', 4)

    std_devs = np.sqrt(np.diag(self.corr))
    outer_std = np.outer(std_devs, std_devs)
    self.corr_matrix = self.corr/outer_std

    if self.type == "gauss":
      self.mv = scipy.stats.multivariate_normal(mean=self.mean, cov=self.corr_matrix)
    elif self.type == "t":            
      self.corr_matrix = self.corr_matrix*(self.df-2)/self.dfu
      self.mv = scipy.stats.multivariate_t(loc=self.mean, shape=self.corr_matrix, df=self.df)
    else:
      raise ValueError(f"Copula type {type} unknown.")

  def sample(self, size):
    x = self.mv.rvs(size=size)
    if self.type == "gauss":
      return scipy.stats.norm.cdf(x)
    elif self.type == "t":
      return scipy.stats.t(self.df).cdf(x)
    else:
      raise ValueError(f"Copula type {type} unknown.")

  def sample_marginals(self, size, distributions):
    if len(distributions) != self.n:
      raise ValueError(f"Expected {self.n} distributions, got {len(distributions)}")

    u = self.sample(size)
    samples = np.zeros_like(u)
    for i, dist in enumerate(distributions):
      if hasattr(dist, "ppf"):
        samples[:, i] = dist.ppf(u[:, i])
      else:
        raise TypeError(f"Element at index {i} must have a .ppf() method.")
    return samples
