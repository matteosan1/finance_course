import numpy as np

from finmarkets import CreditCurve, CreditDefaultSwap, SwapSide

class BasketDefaultSwaps:
    def __init__(self, nominal, N, start_date, maturity, spread, tenor="3m", 
                 recovery=0.4, side=SwapSide.Buyer):
        self.cds = CreditDefaultSwap(nominal, start_date, maturity,
                                     spread, tenor, recovery, side)
        self.N = N
        self.cc = None

    def credit_curve(self, nth_default, copula_func, default_prob, obs_date, 
                     pillars, simulations=100000):
        copula_sample = copula_func.sample(simulations)
        default_times = default_prob.ppf(copula_sample)

        Ts = [(p-obs_date).days/365 for p in pillars]
        ndps = []
        for t in Ts:
            entity_defs_per_sim = np.sum(default_times <= t, axis=1)
            tot_defs = np.sum(entity_defs_per_sim >= nth_default)
            ndps.append(1 - tot_defs/simulations)
        self.cc = CreditCurve(obs_date, pillars, ndps)

    def npv(self, dc):
        if self.cc is None:
            print ("Need to call credit_curve method first !")
            return None
        return self.cds.npv(dc, self.cc)
    
    def breakeven(self, dc):
        if self.cc is None:
            print ("Need to call credit_curve method first !")
            return None
        return self.cds.breakevenRate(dc, self.cc)
