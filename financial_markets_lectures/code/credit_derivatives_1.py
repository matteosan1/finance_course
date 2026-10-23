import numpy as np

from datetime import date
from typing import List, Union, Optional

from dates import yearFraction, TimeInterval, GlobalConsts as gc
from distributions import PoissonProcess
from copulas import Copula
from curves import CreditCurve
from credit import CreditDefaultSwap

class BasketDefaultSwaps:
  def __init__(self, poisson_processes: List[PoissonProcess], m: int, 
               nominal: float, start_date: date, 
               maturity: Union[str, TimeInterval], spread: float, 
               tenor: str="3m", recovery: float=0.4, side: str="Buyer"):
    self.cds = CreditDefaultSwap(nominal, start_date, maturity, 
                                 spread, tenor, recovery, side)       
    self.poisson_processes = poisson_processes
    self.m = m
    self.cc = None

  def credit_curve(self, copula: Copula, 
                   simulations: int=100000, seed: int=1) -> CreditCurve:
    np.random.seed(seed)
    N = len(self.poisson_processes)    
    copula.rvs(size=simulations, seed=seed)
    default_times = copula.rvs_marginals(distributions=self.poisson_processes)
    pillar_times = np.array([yearFraction(gc.OBS_DATE, d) \\
      for d in self.cds.fix_dates], dtype=float)
    joint_ndps = []
    for t in pillar_times:        
        defaults_count = np.sum(default_times <= t, axis=1)
        survived_paths = (defaults_count < self.m)
        joint_survival_prob = np.mean(survived_paths)
        joint_ndps.append(joint_survival_prob)
    self.cc = CreditCurve(pillars=list(self.cds.fix_dates), ndps=joint_ndps)

  def npv(self, dc):
    if self.cc is None:
      print ("Need to call credit_curve method first !")
      return None
    return self.cds.npv(self.cc, dc)
    
  def breakeven_rate(self, dc):
    if self.cc is None:
      print ("Need to call credit_curve method first !")
      return None
    return self.cds.breakeven_rate(self.cc, dc)
