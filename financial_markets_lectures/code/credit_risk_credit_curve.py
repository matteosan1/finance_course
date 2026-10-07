import numpy as np

from scipy.interpolate import interp1d

from finmarkets import GlobalConst as gc
from finmarkets import TimeInterval

class CreditCurve:
  def __init__(self, pillars: Union[List[date], np.array], ndps: Union[List[float], np.array]):
    if len(pillars) != len(ndps):
      raise ValueError("pillars and ndps must have the same length.")
    self.ndps = np.array(ndps, dtype=float) if isinstance(ndps, list) else ndps
    if gc.OBS_DATE not in pillars:
      pillars = [gc.OBS_DATE] + pillars
      self.ndps = np.insert(self.ndps, 0, 1.0)
    self.pillars = pillars
    t_arr = np.array([d.toordinal() for d in self.pillars], dtype=float)
    self.interpolator = interp1d(t_arr, self.ndps, bounds_error=True)

  def ndp(self, d):
    d_days = d.toordinal()
    return self.interpolator(d_days)
    
  def hazard(self, d):
    ndp_1 = self.ndp(d)
    ndp_2 = self.ndp(d + TimeInterval("1d"))
    delta_t = 1.0 / 365.0
    h = -1.0 / ndp_1 * (ndp_2 - ndp_1) / delta_t
    return h

