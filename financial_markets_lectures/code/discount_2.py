import numpy as np

from datetime import date
from scipy.interpolate import interp1d
from typing import Union, List

from finmarkets import GlobalConst as gc
from finmarkets import TimeInterval, yearFraction

class DiscountCurve:
  def __init__(self, pillars: Union[List[date], np.array], 
               discount_factors: Union[List[float], np.array]):
    if len(pillars) != len(discount_factors):
       raise ValueError("pillars and discount_factors must have"
         "the same length.")
    self.day_count_convention = "ACT365"
    self.dfs = np.array(discount_factors, dtype=float) \\
      if isinstance(discount_factors, list) else discount_factors
    self.pillars = pillars
    if gc.OBS_DATE not in pillars:
      self.pillars = [gc.OBS_DATE] + self.pillars
      self.dfs = np.insert(self.dfs, 0, 1.0)
    self.times = np.array([self._get_time(d) for d in self.pillars], 
                           dtype=float)
    self.log_df_interpolator = interp1d(self.times, np.log(self.dfs), 
                                        bounds_error=True)

  def _get_time(self, d: date):
    return yearFraction(gc.OBS_DATE, d, self.day_count_convention)

  def df(self, d: date) -> float:
    t = self._get_time(d)
    if t <= 0.0:
      return 1.0
    log_df_t = self.log_df_interpolator(t)
    return float(np.exp(log_df_t))

  def get_zero_rate(self, d: date, compounding: str="Continuous") -> float:
    t = self._get_time(d)
    if t <= 0.0:
      return 0.0
    df = self.df(d)

    if compounding == "Continuous":
      return -np.log(df) / t
    elif compounding == "Annual":
      return (1.0 / df) ** (1.0 / t) - 1.0
    else:
      raise ValueError(f"Regime non supportato: {compounding}")
