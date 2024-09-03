import numpy as np

from scipy.interpolate import interp1d

class DiscountCurve:
    def __init__(self, obs_date, pillar_dates, discount_factors):
        discount_factors = np.array(discount_factors)
        if obs_date not in pillar_dates:
            pillar_dates = [obs_date] + pillar_dates
            discount_factors = np.insert(discount_factors, 0, 1)
        self.pillar_dates = pillar_dates
        self.pillars = [p.toordinal() for p in pillar_dates] 
        self.log_discount_factors = np.log(discount_factors)
        self.interpolator = interp1d(self.pillars, self.log_discount_factors)
        
    def df(self, adate):
        d = adate.toordinal()
        if d < self.pillars[0] or d > self.pillars[-1]:
            raise ValueError(f"Cannot extrapolate (date: {adate}).")
        return np.exp(self.interpolator(d))