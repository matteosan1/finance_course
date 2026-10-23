import numpy as np, pandas as pd

from scipy.optimize import minimize
from typing import List, Union

class PortfolioOptimizer:
  ...
  def min_variance_portfolio(self, target_return: float=None, 
                             rf: Union[float, None]=None):    
    self.annualized_return_cov()
    num_assets = len(self.assets)
    if rf is not None:
      self.returns['rf'] = rf
      self.covariance['rf'] = 0.0
      self.covariance.loc['rf'] = 0.0
      num_assets += 1
    
    constraints = [{"type": "eq", "fun": self._sum_weights}]
    if target_return is not None:
      constraints.append({"type": "eq", "fun": self._target_return, 
                          "args": [target_return]})

    bounds = [(0.0, 1.0) for _ in range(num_assets)]
    initial_weights = [1.0 / num_assets for _ in range(num_assets)]

    return minimize(self.portfolio_risk, initial_weights, method="SLSQP", 
                    bounds=bounds, constraints=constraints)

  def efficient_frontier(self, targets: Union[List[float], None]=None, 
                         rf: Union[float, None]=None):
    if targets is None:
      targets = np.arange(0.10, 0.40, 0.01)

    results = []
    for target in targets:
      opts = self.min_variance_portfolio(target, rf)
      if opts.success:
        results.append((self.portfolio_risk(opts.x), 
                        self.portfolio_return(opts.x)))
    return np.array(results)

optimizer = PortfolioOptimizer("portfolio_data.csv",
                               assets=['AAPL', 'AMZN', 'FB', 'GOOG', 'NFLX'],
                               index_col="date")
results_rf = optimizer.efficient_frontier(rf=0.10)    