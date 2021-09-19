import math
import numpy
from math import log, exp, sqrt
from scipy.stats import norm
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
 
def plotVectors(vecs, cols, alpha=1):
    plt.figure()
    plt.axvline(x=0, color='#A9A9A9', zorder=0)
    plt.axhline(y=0, color='#A9A9A9', zorder=0)
 
    for i in range(len(vecs)):
        x = numpy.concatenate([[0,0],vecs[i]])
        plt.quiver([x[0]],
                   [x[1]],
                   [x[2]],
                   [x[3]],
                   angles='xy', scale_units='xy', scale=1, color=cols[i],
                   alpha=alpha)

def d1(S_t, K, r, vol, ttm):
    num = log(S_t/K) + (r + 0.5*pow(vol, 2)) * ttm
    den = vol * sqrt(ttm)
    if den == 0:
        return 100000000.
    return num/den

def d2(S_t, K, r, vol, ttm):
    return d1(S_t, K, r, vol, ttm) - vol * sqrt(ttm)

def call(S_t, K, r, vol, ttm):
    return S_t * norm.cdf(d1(S_t, K, r, vol, ttm)) - K * exp(-r * ttm) * norm.cdf(d2(S_t, K, r, vol, ttm))

def put(S_t, K, r, vol, ttm):
    return K * exp(-r * ttm) * norm.cdf(-d2(S_t, K, r, vol, ttm)) - S_t * norm.cdf(-d1(S_t, K, r, vol, ttm))

class DiscountCurve:
    def __init__(self, today, pillar_dates, discount_factors):
        # we just store the arguments as attributes of the instance
        self.today = today
        self.pillar_dates = pillar_dates
        self.discount_factors = discount_factors
        
        self.log_discount_factors = [
            math.log(discount_factor)
            for discount_factor in self.discount_factors
        ]
        
        self.pillar_days = [
            (pillar_date - self.today).days
            for pillar_date in self.pillar_dates
        ]        
        
    def df(self, d):
        d_days = (d - self.today).days
        interpolated_log_discount_factor = numpy.interp(d_days, self.pillar_days, self.log_discount_factors)
        
        return math.exp(interpolated_log_discount_factor) 
    
    def forward_libor(self, d1, d2):
        return (
            self.df(d1) /
            self.df(d2) - 1
        ) / ((d2  - d1).days / 365)

class ForwardRateCurve:
    def __init__(self, today, pillar_dates, rates):
        self.today = today
        self.pillar_dates = pillar_dates
        self.rates = rates

        self.pillar_days = [(pillar_date - self.today).days
            for pillar_date in self.pillar_dates]        

    def interp_rate(self, d):
        d_days = (d - self.today).days
        interpolated_rate = numpy.interp(d_days, self.pillar_days, self.rates)
        return interpolated_rate, d_days/365

    def forward_rate(self, d1, d2):
        if d1 == d2:
            return self.interp_rate(d1)[0]
        else:
            r1, d1_days = self.interp_rate(d1)
            r2, d2_days = self.interp_rate(d2)
            return ((1+r2*d2_days)/(1+r1*d1_days)-1) / (d2_days - d1_days)
        
class OvernightIndexSwap:
    def __init__(self, notional, payment_dates, fixed_rate):
        
        self.notional = notional
        self.payment_dates = payment_dates
        self.fixed_rate = fixed_rate

    def __str__(self):
        s = "This is an OvernightIndexSwap with a notional of {}\n".format(self.notional)
        s += "And the following payment_dates {}".format(self.payment_dates)
        return s
        
    def npv_floating_leg(self, discount_curve):
        
        return self.notional * (
             discount_curve.df(self.payment_dates[0]) - 
             discount_curve.df(self.payment_dates[-1])      
        )
    
    def npv_fixed_leg(self, discount_curve):
        
        npv = 0
        for i in range(1, len(self.payment_dates)):   
            
            start_date = self.payment_dates[i-1]
            end_date = self.payment_dates[i]
            
            tau = (end_date - start_date).days / 365
            df = discount_curve.df(end_date)
            
            npv = npv + df * tau
            
        return self.notional * self.fixed_rate * npv
    
    def npv(self, discount_curve):
        
        float_npv = self.npv_floating_leg(discount_curve)
        fixed_npv = self.npv_fixed_leg(discount_curve)
        
        return float_npv - fixed_npv
    
    
def generate_dates(start_date, n_months, tenor_months=12):
    
    dates = []
    for n in range(0, int(n_months), int(tenor_months)):
        dates.append(start_date + relativedelta(months=n))
    dates.append(start_date + relativedelta(months=n_months))
    
    return dates    

class InterestRateSwap:
    def __init__(self, obs_date, start_date, nominal, fixed_rate, tenor_months, maturity_years):
        self.nominal = nominal
        self.obs_date = obs_date
        self.fixed_rate = fixed_rate
        self.fixed_leg_dates = generate_dates(start_date, 12 * maturity_years, 
                                                   tenor_months)
        self.floating_leg_dates = generate_dates(start_date, 12 * maturity_years,
                                                      tenor_months)
        
    def fixed_leg(self, discount_curve):
        s = 0
        for j in range(1, len(self.fixed_leg_dates)):
            tau = (self.fixed_leg_dates[j] - self.fixed_leg_dates[j-1]).days / 360
            D = discount_curve.df(self.fixed_leg_dates[j])
            s += self.fixed_rate * tau * D
        return self.nominal * s

    def floating_leg(self, discount_curve, libor_curve):
        s = 0
        for j in range(1, len(self.floating_leg_dates)):
            if self.obs_date == 1:
                F = 1/discount_curve.df(self.floating_leg_dates[j])
            else:
                F = libor_curve.forward_rate(self.floating_leg_dates[0], self.floating_leg_dates[j+1])
            tau = (self.floating_leg_dates[j] - self.floating_leg_dates[j-1]).days / 360
            D = discount_curve.df(self.floating_leg_dates[j])
            s += F * tau * D
        return self.nominal*s
        
    def annuity(self, discount_curve, start_date=None):
        a = 0
        for i in range(1, len(self.fixed_leg_dates)):
            if start_date is None or start_date < self.fixed_leg_dates[i]:
                a += discount_curve.df(self.fixed_leg_dates[i])
        return a

    def num(self, discount_curve, libor_curve):
        s = 0
        for j in range(1, len(self.floating_leg_dates)):
            F = libor_curve.forward_rate(self.floating_leg_dates[j], self.floating_leg_dates[j-1])
            tau = (self.floating_leg_dates[j] - self.floating_leg_dates[j-1]).days / 360
            D = discount_curve.df(self.floating_leg_dates[j])
            s += F * tau * D
        return s
    
    def swap_rate(self, discount_curve, libor_curve):
        return self.num(discount_curve, libor_curve) / self.annuity(discount_curve)

    def spread(self, discount_curve, libor_curve):
        s = self.num(discount_curve, libor_curve)

        den = 0
        for j in range(1, len(self.floating_leg_dates)):
            tau = (self.floating_leg_dates[j] - self.floating_leg_dates[j-1]).days / 360
            D = discount_curve.df(self.floating_leg_dates[j])
            den += tau * D
            
        return (self.annuity(discount_curve)*self.fixed_rate - s)/(den)
        
    def npv(self, discount_curve, libor_curve):
        S = self.swap_rate(discount_curve, libor_curve)
        A = self.annuity(discount_curve)
        return self.nominal * (S - self.fixed_rate) * A

class InterestRateSwaption:
    
    def __init__(self, exercise_date, irs):
        self.exercise_date = exercise_date
        self.irs = irs
        
    def npv_bs(self, discount_curve, libor_curve, sigma):
        
        A = self.irs.annuity(discount_curve)
        S = self.irs.swap_rate(discount_curve, libor_curve)

        T = (self.exercise_date - discount_curve.today).days / 365

        d1 = (math.log(S/self.irs.fixed_rate) + 0.5 * sigma**2 * T) / (sigma * T**0.5)
        d2 = d1 - (sigma * T**0.5)

        npv = self.irs.nominal * A * (S * scipy.stats.norm.cdf(d1) - 
                                      self.irs.fixed_rate * scipy.stats.norm.cdf(d2))
        
        return npv
    
    def npv_mc(self, discount_curve, libor_curve, sigma, n_scenarios=10000):
        
        A = self.irs.annuity(discount_curve)
        S = self.irs.swap_rate(discount_curve, libor_curve)
        T = (self.exercise_date - discount_curve.today).days / 365
        discounted_payoffs = []

        for i_scenario in range(n_scenarios):
            rnd =  numpy.random.normal()
            S_simulated = S * math.exp(-0.5 * sigma * sigma * T +
                                       sigma * math.sqrt(T) * rnd)
            swap_npv = self.irs.nominal * (S_simulated - self.irs.fixed_rate) * A
            #discounted_payoffs.append(max(0, swap_npv))
            discounted_payoffs.append(swap_npv)

        npv_mc = numpy.mean(discounted_payoffs)
        npv_error = 3 * numpy.std(discounted_payoffs) / math.sqrt(n_scenarios)
        
        return npv_mc, npv_error

class CreditCurve:
    
    def __init__(self, pillar_dates, pillar_ndps):
        
        self.pillar_dates = pillar_dates
        self.pillar_ndps = pillar_ndps
        
        self.pillar_days = [
            (pd - pillar_dates[0]).days
            for pd in pillar_dates
        ]
        
        self.log_ndps = [
            math.log(ndp)
            for ndp in pillar_ndps
        ]
        
    def ndp(self, value_date):
        
        value_days = (value_date - self.pillar_dates[0]).days
        
        return math.exp(
            numpy.interp(
                value_days,
                self.pillar_days,
                self.log_ndps
            )
        )
    
    def hazard(self, value_date):
               
        ndp_1 = self.ndp(value_date)
        ndp_2 = self.ndp(value_date + relativedelta(days=1))
        delta_t = 1.0 / 365.0
        h = -1.0 / ndp_1 * (ndp_2 - ndp_1) / delta_t
        return h
    
class CreditDefaultSwap:
    def __init__(self, notional, start_date, nyears, fixed_spread, recovery=0.4):
        self.notional = notional
        self.payment_dates = generate_dates(start_date, nyears*12, 3)
        self.fixed_spread = fixed_spread
        self.recovery = recovery

    def premium_leg_npv(self, discount_curve, credit_curve):
        npv = 0
        for i in range(1, len(self.payment_dates)):
            npv += (
                self.fixed_spread *
                discount_curve.df(self.payment_dates[i]) *
                credit_curve.ndp(self.payment_dates[i])
            )

        return npv * self.notional

    def default_leg_npv(self, discount_curve, credit_curve):
        npv = 0
        d = self.payment_dates[0]
        while d <= self.payment_dates[-1]:
            npv += discount_curve.df(d) * (
                credit_curve.ndp(d) -
                credit_curve.ndp(d + relativedelta(days=1))
            )
            d += relativedelta(days=1)
        return npv * self.notional * (1 - self.recovery)

    def npv(self, discount_curve, credit_curve):
        return self.default_leg_npv(discount_curve, credit_curve) - \
               self.premium_leg_npv(discount_curve, credit_curve)
 
