import numpy as np

from scipy.stats import norm

from finmarkets import GlobalConst as gc
from finmarkets import InterestRateSwap, yearFraction

class InterestRateSwaption:
  def __init__(self, nominal, start_date, exercise_date, maturity,\
               volatility, fixed_rate, frequency_float, frequency_fix="1y", side="Payer"):
    self.irs = InterestRateSwap(nominal, exercise_date, maturity, fixed_rate,
                                frequency_float, frequency_fix, side)
    self.exercise_date = exercise_date
    self.sigma = volatility
    self.side = 1 if side == "Receiver" else -1

  def npv_Black(self, dc, fr):
    T = yearFraction(gc.OBS_DATE, self.exercise_date, "ACT360")
    K = self.irs.fixed_rate
    S = self.irs.swap_rate(dc, fr)
    dp = (np.log(S/K) + 0.5*self.sigma**2*T)/(self.sigma*np.sqrt(T))
    dm = (np.log(S/K) - 0.5*self.sigma**2*T)/(self.sigma*np.sqrt(T))
    return self.irs.nominal*self.irs.annuity(dc)*(S*norm.cdf(dp)-K*norm.cdf(dm))
