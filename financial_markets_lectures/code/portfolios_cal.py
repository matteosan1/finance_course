import numpy as np, pandas as pd

from scipy.optimize import minimize
from typing import List, Union

class PortfolioOptimizer:
  ...
  def portfolio_return(self, w: np.array) -> float:
    if self.rf_return > 0:
      return float(np.dot(w[:-1], self.returns)) + self.rf_return * w[-1]
    else:
      return float(np.dot(w, self.returns))

  def portfolio_risk(self, w: np.array) -> float:
    if self.rf_return > 0:
      w = w[:-1]
    return float(np.sqrt(w.T @ self.covariance @ w))

  def min_variance_portfolio(self, target_return: float):
    num_assets = len(self.assets)
    if self.rf_return > 0:
      num_assets += 1

    constraints = [{"type": "eq", "fun": self._sum_weights},
                   {"type": "eq", "fun": self._target_return, 
                    "args": (target_return,)},]

    bounds = tuple((0.0, 1.0) for _ in range(num_assets))
    initial_weights = [1.0 / num_assets for _ in range(num_assets)]
    return minimize(self.portfolio_risk, initial_weights, method="SLSQP", 
                    bounds=bounds, constraints=constraints)
  ...

optimizer = PortfolioOptimizer("portfolio_data.csv",
                               assets=['AAPL', 'AMZN', 'FB', 'GOOG', 'NFLX'],
                               rf_return=0.1, index_col="date")
results_rf = optimizer.efficient_frontier()    