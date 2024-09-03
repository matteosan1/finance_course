from scipy.interpolate import interp1d

class TermStructure:
    def __init__(self, obs_date, pillars, rates):
        self.obs_date = obs_date
        self.pillars = [(p-self.obs_date).days/365 for p in pillars]
        self.rates = rates
        self.interpolator = interp1d(self.pillars, self.rates)

    def interp_rate(self, adate):
        yf = (adate-self.obs_date).days/365
        if yf < self.pillars[0] or yf > self.pillars[-1]:
            raise ValueError(f"Cannot extrapolate rates (date: {adate}).")
        return yf, self.interpolator(yf)

    def forward_rate(self, d1, d2):
        yf1, r1 = self.interp_rate(d1)
        yf2, r2 = self.interp_rate(d2)
        return (r2*yf2 - r1*yf1)/(yf2 - yf1)