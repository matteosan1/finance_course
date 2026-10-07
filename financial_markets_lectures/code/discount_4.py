import numpy as np

from scipy.interpolate import interp1d
from typing import Union, List

from dates import GlobalConsts as gc, yearFraction

class TermStructure:
  def __init__(self, pillars: Union[np.array, List[date]], 
               rates: Union[np.array, List[float]], 
               day_count_convention = "ACT360"):
    if len(pillars) != len(rates):
      raise ValueError("pillars and rates must have the same the length.")

    self.day_count_convention = day_count_convention
    times = np.array([self._get_time(p) for p in pillars], dtype=float)
    self.rates = np.array(rates, dtype=float) \\
      if isinstance(rates, list) else rates
    self.pillars = pillars
    self.interpolator = interp1d(times, self.rates, bounds_error=True)
    
  def _get_time(self, d: date) -> float:
    return yearFraction(gc.OBS_DATE, d, self.day_count_convention)

  def interp_rate(self, adate: date) -> tuple[float, float]:
    d = yearFraction(gc.OBS_DATE, adate, self.day_count_convention)
    return float(d), float(self.interpolator(d))

  def forward_rate(self, d1: date, d2: date) -> float:
    if d1 > d2:
      raise ValueError("d1 must be lower than d2.")
            
    t1, r1 = self.interp_rate(d1)
    t2, r2 = self.interp_rate(d2)
    return float((r2*t2 - r1*t1)/(t2-t1))