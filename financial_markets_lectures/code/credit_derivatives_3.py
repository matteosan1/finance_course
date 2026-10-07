import numpy as np

from finmarkets import CreditCurve, CreditDefaultSwap

import numpy as np
from datetime import date
from typing import List, Union, Optional

class BasketDefaultSwaps:
  def __init__(self, nominal, N, start_date, maturity, spread, tenor="3m", 
               recovery=0.4, side="Buyer"):
    self.cds = CreditDefaultSwap(nominal, start_date, maturity,
                                 spread, tenor, recovery, side)
    self.N = N
    self.cc = None

  def credit_curve(lambdas_list: List[Union[float, np.ndarray]], 
                   times_list: Optional[List[Optional[np.ndarray]]] = None,
                   M: int, pillars: List[date],
                   copula_type: str = "gauss", copula_params: dict, 
                   n_scenarios: int = 100000, seed: Optional[int] = None) -> CreditCurve:
    N = len(lambdas_list)
    if not (1 <= M <= N):
      raise ValueError(f"M must be between 1 and N={N}, got M={M}.")
      
    if seed is not None:
      np.random.seed(seed)
  
    distributions = []
    for i in range(N):
      lmb = lambdas_list[i]
      tm = times_list[i] if times_list is not None else None
      dist = PoissonProcess(lambdas=lmb, times=tm)
      distributions.append(dist)    
      copula = Copula(n=N, typ=copula_type, params=copula_params)    
      default_times = copula.sample_marginals(size=n_scenarios, distributions=distributions)
      sorted_default_times = np.sort(default_times, axis=1)
      tau_M = sorted_default_times[:, M-1]
      ndps = []
      for p in pillars:
        t_years = yearFraction(gc.OBS_DATE, p, "ACT365")
        if t_years <= 0:
          ndps.append(1.0)
        else:
          ndp_m = float(np.mean(tau_M > t_years))
          ndps.append(ndp_m)
      self.cc = CreditCurve(pillars=pillars, ndps=ndps)

  def npv(self, dc):
    if self.cc is None:
      print ("Need to call credit_curve method first !")
      return None
    return self.cds.npv(dc, self.cc)
    
  def breakeven(self, dc):
    if self.cc is None:
      print ("Need to call credit_curve method first !")
      return None
    return self.cds.breakevenRate(dc, self.cc)
