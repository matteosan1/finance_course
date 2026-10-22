import numpy as np

from datetime import date
from scipy.stats import norm
from typing import Union

from dates import GlobalConsts as gc, TimeInterval, yearFraction
from curves import DiscountCurve, TermStructure
from ird import InterestRateSwap
from short_rate import VasicekModel

class Swaption:
  def __init__(self, start_date: date, exercise_date: date, 
               swap: InterestRateSwap):
    self.swap = swap
    self.start_date = start_date
    self.exercise_date = exercise_date

  def npv_Black(self, sigma: float, dc: DiscountCurve, fr: TermStructure) -> float:
    T = yearFraction(gc.OBS_DATE, self.exercise_date, "ACT360")
    K = self.swap.fixed_rate
    S = self.swap.swap_rate(dc, fr)
    dp = (np.log(S/K) + 0.5*sigma**2*T)/(sigma*np.sqrt(T))
    dm = (np.log(S/K) - 0.5*sigma**2*T)/(sigma*np.sqrt(T))

    if self.swap.side == -1:        
        payoff = S * norm.cdf(dp) - K * norm.cdf(dm)
    else:
        payoff = K * norm.cdf(-dm) - S * norm.cdf(-dp)
    return self.swap.nominal*self.swap.annuity(dc)*payoff

  def npv(self, N: int, r0: float, dt: float, 
          model_d: Union[VasicekModel], model_f: Union[VasicekModel]=None, 
          seed: int=1) -> float:
    if model_f is None:
      model_f = model_d          
    T_opt = yearFraction(self.start_date, self.exercise_date, 
                         self.swap.day_count_convention)
    r_paths = model_d.simulate_r(r0, N, T_opt, dt, seed=seed)
    r_opt = r_paths[:, -1]

    integral_r = np.sum(r_paths[:, :-1], axis=1) * dt
    df_to_topt = np.exp(-integral_r)

    tau_payments = np.array([yearFraction(self.exercise_date, d, 
                   self.swap.day_count_convention) for d in self.swap.float_dates])
    payoffs = np.zeros(N)

    gc.OBS_DATE = self.exercise_date
    for i in range(N):
      r_val = r_opt[i]
      df_path = np.array([model_d.P(r_val, tau) for tau in tau_payments])
      rates_path = np.array([model_f.R(r_val, tau) for tau in tau_payments])
      discount_curve = DiscountCurve(pillars=self.swap.float_dates, 
                                     discount_factors=df_path, 
                                     eval_date=self.exercise_date)
      term_structure = TermStructure(pillars=self.swap.float_dates, 
                                     rates=rates_path, 
                                     eval_date=self.exercise_date)
      payoffs[i] = max(self.swap.npv(discount_curve, term_structure), 0.0)
    gc.OBS_DATE = self.start_date    
    swaption_price = np.mean(df_to_topt * payoffs)
    cl = np.std(df_to_topt * payoffs)/np.sqrt(N)*1.96
    return swaption_price, cl