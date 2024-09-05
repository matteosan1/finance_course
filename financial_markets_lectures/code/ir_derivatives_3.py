import numpy as np

from scipy.stats import norm
from finmarkets import SwapSide, InterestRateSwap

class InterestRateSwaption:
    def __init__(self, nominal, start_date, exercise_date, maturity,\
                 volatility, fixed_rate, frequency_float, frequency_fix="1y",\
                 side=SwapSide.Payer):
        self.irs = InterestRateSwap(nominal, exercise_date, maturity, fixed_rate,
                                    frequency_float, frequency_fix, side)
        self.exercise_date = exercise_date
        self.sigma = volatility

    def npv_Black(self, obs_date, dc, fr):
        T = (self.exercise_date - obs_date).days/365
        N = self.irs.nominal
        K = self.irs.fixed_rate
        S = self.irs.swap_rate(dc, fr)
        A = self.irs.annuity(dc)
        dp = (np.log(S/K) + 0.5*self.sigma**2*T)/(self.sigma*np.sqrt(T))
        dm = (np.log(S/K) - 0.5*self.sigma**2*T)/(self.sigma*np.sqrt(T))
        return N*A*(S*norm.cdf(dp)-K*norm.cdf(dm))
