import numpy as np

from finmarkets import CreditCurve, CreditDefaultSwap
from scipy.stats import norm, binom
from scipy.integrate import quad

class BasketDefaultSwapsOneFactor:
    def __init__(self, nominal, N, rho, start_date, maturity,
                 spread, tenor="3m", recovery=0.4):
        self.N = N
        self.rho = rho
        self.cds = CreditDefaultSwap(nominal, start_date, maturity,
                                     spread, tenor, recovery)

    def one_factor_model(self, M, f, obs_date,
                         Q_dates, Q, dc, ndefaults):
        P = norm.cdf((norm.ppf(Q) - np.sqrt(self.rho)*M)/np.sqrt(1-self.rho))
        b = binom(self.N, P)
        S = 1 - (1 - b.cdf(ndefaults-1))
        cc = CreditCurve(obs_date, Q_dates, S)
        return f(dc, cc)*norm.pdf(M)
            
    def breakeven(self, obs_date, Q_dates, Q, dc, ndefaults):
        s = quad(self.one_factor_model, -np.inf, np.inf, 
                 args=(self.cds.breakevenRate, Q_dates, Q, dc, ndefaults))
        return s[0]
    
    def npv(self, obs_date, Q_dates, Q, dc, ndefaults):
        s = quad(self.one_factor_model, -np.inf, np.inf, 
                 args=(self.cds.npv, Q_dates, Q, dc, ndefaults))
        return s[0] 