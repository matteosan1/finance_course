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
