import numpy as np, pandas as pd

from scipy.optimize import minimize
from typing import List, Union

class PortfolioOptimizer:
  def __init__(self, filename: str, assets: List[str], 
               rf_return: float=0.0, index_col: str="date"):
    self.assets = assets
    self.rf_return = float(rf_return)

    temp = pd.read_csv(filename, index_col=index_col)
    temp = temp[self.assets].dropna()
    log_returns = np.log(temp / temp.shift(1)).dropna()

    self.df = temp
    self.returns = log_returns.mean() * 252
    self.covariance = log_returns.cov() * 252

  def _sum_weights(self, w: np.array) -> float:
    return np.sum(w) - 1.0

  def _target_return(self, w: np.array, target: float) -> float:
    return self.portfolio_return(w) - target

  def portfolio_return(self, w: np.array) -> float:
    return float(np.dot(w, self.returns))

  def portfolio_risk(self, w: np.array) -> float:
    return float(np.sqrt(w.T @ self.covariance @ w))

  def min_variance_portfolio(self, target_return: float):
    num_assets = len(self.assets)

    constraints = [{"type": "eq", "fun": self._sum_weights},
                   {"type": "eq", "fun": self._target_return, 
                    "args": (target_return,)},]

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
