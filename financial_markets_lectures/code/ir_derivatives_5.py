class InterestRateSwaption:
    ....

  def npv_MC(self, dc, fr, n_scenarios=100000, seed=1):
    T = yearFraction(gc.OBS_DATE, self.exercise_date, "ACT360")
    S0 = self.irs.swap_rate(dc, fr)
    annuity = self.irs.annuity(dc)

    np.random.seed(seed)
    Z = norm.rvs(size=n_scenarios)    
    S = S0 * np.exp(-0.5 * (self.sigma ** 2) * T + self.sigma * np.sqrt(T) * Z)
    payoffs = np.maximum(0, self.side * (S - self.irs.fixed_rate))    
    npvs = self.irs.nominal * annuity * payoffs
    
    npv = np.mean(npvs)
    std_err = np.std(npvs, ddof=1) / np.sqrt(n_scenarios)
    interval = 1.96 * std_err    
    return npv, interval
