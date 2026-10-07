class PortfolioOptimizer:
  ...
  def _sharpe_ratio(self, w: np.array):
    p_ret = self.portfolio_return(w)
    p_vol = self.portfolio_risk(w)
    if p_vol < 1e-8:
      return 0.0
    return -(p_ret - self.rf_return) / p_vol

  def sharpe_portfolio(self):
    num_assets = len(self.assets)
    if self.rf_return > 0:
      num_assets += 1

    constraints = [{"type": "eq", "fun": self._sum_weights}]
    bounds = [(0.0, 1.0) for _ in range(num_assets)]

    if self.rf_return > 0:
      bounds[-1] = (0.0, 0.0)

    initial_weights = [1.0 / num_assets for _ in range(num_assets)]
    return minimize(self._sharpe_ratio, initial_weights, method="SLSQP", 
                    bounds=bounds, constraints=constraints)

optimizer = PortfolioOptimizer("portfolio_data.csv",
                               assets=['AAPL', 'AMZN', 'FB', 'GOOG', 'NFLX'],
                               rf_return=0.1, index_col="date")

opts = optimizer.sharpe_portfolio()
print (opts)
ret = optimizer.portfolio_return(opts.x)
vol = optimizer.portfolio_risk(opts.x)
print (f"Sharpe ratio: {-opts.fun:.3f}")
