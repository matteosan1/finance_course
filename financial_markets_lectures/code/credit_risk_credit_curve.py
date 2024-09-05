import numpy as np

from scipy.interpolate import interp1d
from dateutil.relativedelta import relativedelta

class CreditCurve:
    def __init__(self, obs_date, pillars, ndps):
        self.obs_date = obs_date
        if obs_date not in pillars:
            pillars = [obs_date] + pillars
            ndps = np.insert(ndps, 0, 1)
        self.pillars = [d.toordinal() for d in pillars]
        self.ndps = ndps
        self.interpolator = interp1d(self.pillars, self.ndps)
        
    def ndp(self, d):
        d_days = d.toordinal()
        if d_days < self.pillars[0] or d_days > self.pillars[-1]:
            raise ValueError(f"Cannot extrapolate Psur (date: {d}).")0
        return self.interpolator(d_days)
    
    def hazard(self, d):
        ndp_1 = self.ndp(d)
        ndp_2 = self.ndp(d + relativedelta(days=1))
        if ndp_1 is None or ndp_2 is None:
            return None
        delta_t = 1.0 / 365.0
        h = -1.0 / ndp_1 * (ndp_2 - ndp_1) / delta_t
        return h
