class PortfolioOptimizer:
  ...
  def _sharpe_ratio(self, w: np.array, rf: float) -> float:
    p_ret = self.portfolio_return(w)
    p_vol = self.portfolio_risk(w)
    if p_vol < 1e-8:
      return 0.0
    return -(p_ret - self.rf_return) / p_vol

  def sharpe_portfolio(self, rf: float):
    self.annualized_return_cov()
    num_assets = len(self.assets)
    
    constraints = [{"type": "eq", "fun": self._sum_weights}]
    bounds = [(0.0, 1.0) for _ in range(num_assets)]

    initial_weights = [1.0 / num_assets for _ in range(num_assets)]
    return minimize(self._sharpe_ratio, initial_weights, method="SLSQP", 
                    bounds=bounds, constraints=constraints, args=[rf])

optimizer = PortfolioOptimizer("portfolio_data.csv",
                               assets=['AAPL', 'AMZN', 'FB', 'GOOG', 'NFLX'],
                               index_col="date")

opts = optimizer.sharpe_portfolio(rf=0.10)
print (opts)
ret = optimizer.portfolio_return(opts.x)
vol = optimizer.portfolio_risk(opts.x)
print (f"Sharpe ratio: {-opts.fun:.3f}")
