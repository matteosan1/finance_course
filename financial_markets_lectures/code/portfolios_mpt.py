import numpy as np, pandas as pd

from scipy.optimize import minimize
from typing import List, Union

class PortfolioOptimizer:
  def __init__(self, filename: str, assets: List[str], index_col: str="date"):
    self.assets = assets
    if df.index.name != index_col:
      df.set_index(index_col, inplace=True)
    df = df[self.assets].dropna()
    self.df = np.log(df / df.shift(1)).dropna()
    self.returns = None
    self.covariance = None
    
  def annualized_return_cov(self):
    self.returns = log_returns.mean() * 252
    self.covariance = log_returns.cov() * 252

  def portfolio_return(self, w: np.array) -> float:
    return np.dot(w, self.returns)

  def portfolio_risk(self, w: np.array) -> float:
    return np.sqrt(w.T @ self.covariance @ w) # np.sqrt(w.T.dot(self.covariance.dot(w)))

  def _sum_weights(self, w: np.array) -> float:
    return np.sum(w) - 1.0

  def _target_return(self, w: np.array, target: float) -> float:
    return self.portfolio_return(w) - target
  
  def min_variance_portfolio(self, target_return: float=None):
    self.annualized_return_cov()
    num_assets = len(self.assets)
    
    constraints = [{"type": "eq", "fun": self._sum_weights}]
    if target_return is not None:
      constraints.append({"type": "eq", "fun": self._target_return, 
                          "args": (target_return,)})

    bounds = tuple((0.0, 1.0) for _ in range(num_assets))
    initial_weights = [1.0 / num_assets for _ in range(num_assets)]
    
    return minimize(self.portfolio_risk, initial_weights, method="SLSQP", 
                    bounds=bounds, constraints=constraints)

optimizer = PortfolioOptimizer("portfolio_data.csv",
                               assets=['AAPL', 'AMZN', 'FB', 'GOOG', 'NFLX'],
                               index_col="date")

opts = optimizer.min_variance_portfolio(0.25)
print (opts)
print (f"Expected portfolio return: {optimizer.portfolio_return(opts.x):.3f}")
