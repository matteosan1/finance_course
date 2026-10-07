class PortfolioOptimizer:
  ...
  def efficient_frontier(self, targets: Union[List[float], None]=None):
    if targets is None:
      targets = np.arange(0.10, 0.40, 0.01)

    results = []
    for target in targets:
      opts = self.min_variance_portfolio(target)
      if opts.success:
        results.append((self.portfolio_risk(opts.x), 
                        self.portfolio_return(opts.x)))
    return np.array(results) 
