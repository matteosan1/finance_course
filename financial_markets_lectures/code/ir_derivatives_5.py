import numpy as np

from scipy.stats import norm

from finmarkets import InterestRateSwap, SwapSide

class InterestRateSwaption:
    ....

    def npv_MC(self, obs_date, dc, fr, n_scenarios=100000):
        T = (self.exercise_date - obs_date).days/365
        npvs = []
        S0 = self.irs.swap_rate(dc, fr)
        for _ in range(n_scenarios):
            S = S0 * np.exp(-self.sigma**2/2*T +\
                            self.sigma*np.random.normal()*np.sqrt(T))
            res = self.irs.nominal*max(0, S - self.irs.fixed_rate)*\
                  self.irs.annuity(dc)
            npvs.append(res)
        npv = np.mean(npvs)
        interval = 1.96*np.std(npvs)/np.sqrt(n_scenarios)
        return npv, interval
