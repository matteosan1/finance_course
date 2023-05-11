from math import exp, log, sqrt
from scipy.stats import norm
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np

def d1(S, K, sigma, r, deltaT):
	return 1/(sigma*sqrt(deltaT))*(log(S/K)+(r+sigma**2/2)*deltaT)
	
def d2(S, K, sigma, r, deltaT):
	return d1(S, K, sigma, r, deltaT) - sigma*sqrt(deltaT)
	
def call(S, K, sigma, r, deltaT):
	return norm.cdf(d1(S, K, sigma, r, deltaT))*S - K*norm.cdf(d2(S, K, sigma, r, deltaT))*exp(-r*deltaT)
	
def put(S, K, sigma, r, deltaT):
	return K*norm.cdf(-d2(S, K, sigma, r, deltaT))*exp(-r*deltaT) - norm.cdf(-d1(S, K, sigma, r, deltaT))*S

def generate_dates(start_date, maturity_months):
  dates = []
  for i in range(0, maturity_months, 12):
    dates.append(start_date + relativedelta(months=i))
  dates.append(start_date + relativedelta(months=maturity_months))
  return dates

class DiscountCurve:
  def __init__(self, pillars, dfs):
    self.start_date = pillars[0]
    self.pillar_days = [(p - pillars[0]).days for p in pillars]
    self.dfs_log = [log(df) for df in dfs]

  def df(self, d):
    d_days = (d - self.start_date).days
    factor = np.interp(d_days, self.pillar_days, self.dfs_log)
    return exp(factor)

class ForwardRateCurve:
  def __init__(self, pillars, rates):
    self.start_date = pillars[0]
    self.pillar_days = [(p-pillars[0]).days/365 for p in pillars]
    self.rates = rates

  def interpolate(self, d):
    d_frac = (d-self.start_date).days/365
    return d_frac, np.interp(d_frac, self.pillar_days, self.rates)

  def forward_rate(self, d1, d2):
    d1_frac, r1 = self.interpolate(d1)
    d2_frac, r2 = self.interpolate(d2)
    return (r2*d2_frac - r1*d1_frac)*(d2_frac - d1_frac)
    
class OvernightIndexSwap:
    def __init__(self, nominal, start_date, fixed_rate, maturity_months):
        self.start_date = start_date
        self.nominal = nominal
        self.fixed_rate = fixed_rate
        self.payment_dates = generate_dates(start_date, maturity_months)
        
    def npv_floating(self, dc):
        return self.nominal * (dc.df(self.payment_dates[0]) - dc.df(self.payment_dates[-1]))
    
    def npv_fixed(self, dc):
        val = 0
        for i in range(1, len(self.payment_dates)):
            val += dc.df(self.payment_dates[i]) * \
                   (self.payment_dates[i] - self.payment_dates[i-1]).days/360 
        return self.nominal*self.fixed_rate*val
    
    def npv(self, dc):
        return self.npv_floating(dc) - self.npv_fixed(dc)