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

def generate_dates(start_date, maturity_months, tenor=12):
        dates = []
        for i in range(0, maturity_months, tenor):
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
                return (r2*d2_frac - r1*d1_frac)/(d2_frac - d1_frac)
        
class OvernightIndexSwap:
        def __init__(self, notional, payment_dates, fixed_rate):
                self.notional = notional 
                self.payment_dates = payment_dates
                self.fixed_rate = fixed_rate
        
        def npv_floating_leg(self, discount_curve):
                return self.notional * (discount_curve.df(self.payment_dates[0]) -
                                        discount_curve.df(self.payment_dates[-1]))

        def npv_fixed_leg(self, discount_curve):
                npv = 0
                for i in range(1, len(self.payment_dates)):
                        start_date = self.payment_dates[i-1]
                        end_date = self.payment_dates[i]
                        tau = (end_date - start_date).days / 360
                        df = discount_curve.df(end_date)
                        npv = npv + df * tau
                return self.notional * self.fixed_rate * npv

        def npv(self, discount_curve):
                float_npv = self.npv_floating_leg(discount_curve)
                fixed_npv = self.npv_fixed_leg(discount_curve)
                return float_npv - fixed_npv

        def fair_value_strike(self, discount_curve):
                den = 0
                for i in range(1, len(self.payment_dates)):
                        start_date = self.payment_dates[i-1]
                        end_date = self.payment_dates[i]
                        tau = (end_date - start_date).days / 360
                        df = discount_curve.df(end_date)
                        den += df * tau
                        num = (discount_curve.df(self.payment_dates[0]) -
                               discount_curve.df(self.payment_dates[-1]))
                return num/den

class InterestRateSwap:
        def __init__(self, start_date, notional,
                     fixed_rate, tenor_months, maturity_years):
                self.start_date = start_date
                self.notional = notional
                self.fixed_rate = fixed_rate
                self.fixed_leg_dates = \
                        generate_dates(start_date, 12 * maturity_years)
                self.floating_leg_dates = \
                        generate_dates(start_date, 12 * maturity_years, tenor_months)
        
        def annuity(self, discount_curve):
                a = 0
                for i in range(1, len(self.fixed_leg_dates)):
                        a += discount_curve.df(self.fixed_leg_dates[i])
                return a

        def swap_rate(self, discount_curve, euribor_curve):
                s = 0
                for j in range(1, len(self.floating_leg_dates)):
                        F = euribor_curve.forward_rate(pricing_date, self.floating_leg_dates[j-1])
                        tau = (self.floating_leg_dates[j] - \
                               self.floating_leg_dates[j-1]).days / 360 
                        P = discount_curve.df(self.floating_leg_dates[j])
                        s += F * tau * P
                return s / self.annuity(discount_curve)

        def npv(self, discount_curve, euribor_curve):
                S = self.swap_rate(discount_curve, euribor_curve, pricing_date)
                A = self.annuity(discount_curve, pricing_date)
                return self.notional * (S - self.fixed_rate) * A

def npvSwaptionBS(pricing_date, irs, sigma, discount_curve, euribor_curve, T):
        A = irs.annuity(discount_curve, pricing_date)
        S = irs.swap_rate(discount_curve, euribor_curve, pricing_date)
        K = irs.fixed_rate
        N = irs.notional
        d_plus = (log(S/K) + 0.5 * sigma**2 * T) / (sigma * T**0.5)
        d_minus = (log(S/K) - 0.5 * sigma**2 * T) / (sigma * T**0.5)
        return irs.notional * A * (S * norm.cdf(d_plus) - K * norm.cdf(d_minus))

class CreditCurve:
        def __init__(self, pillar_dates, ndps):
                self.start_date = pillar_dates[0]
                self.pillar_days = [(pd - self.start_date).days for pd in pillar_dates]
                self.ndps = ndps
        
        def ndp(self, value_date):
                value_days = (value_date - self.start_date).days
                return np.interp(value_days, self.pillar_days, self.ndps)

        def hazard(self, value_date):
                ndp_1 = self.ndp(value_date)
                ndp_2 = self.ndp(value_date + relativedelta(days=1))
                delta_t = 1.0 / 365.0
                h = -1.0 / ndp_1 * (ndp_2 - ndp_1) / delta_t
                return h

class CreditDefaultSwap:
        def __init__(self, notional, start_date, fixed_spread,
                     maturity_y, tenor=3, recovery=0.4):
                self.notional = notional
                self.payment_dates = generate_dates(start_date,
                                                    maturity_y*12, tenor)
                self.fixed_spread = fixed_spread
                self.recovery = recovery
        
        def npv_premium_leg(self, discount_curve, credit_curve):
                npv = 0
                for i in range(1, len(self.payment_dates)):
                        npv += (self.fixed_spread *
                                discount_curve.df(self.payment_dates[i]) *
                                credit_curve.ndp(self.payment_dates[i]))
                return npv * self.notional

        def npv_default_leg(self, discount_curve, credit_curve):
                npv = 0
                d = self.payment_dates[0]
                while d <= self.payment_dates[-1]:
                        npv += discount_curve.df(d) * (
                                credit_curve.ndp(d) -
                                credit_curve.ndp(d + relativedelta(days=1)))
                        d += relativedelta(days=1)
                return npv * self.notional * (1 - self.recovery)

        def npv(self, discount_curve, credit_curve):
                return self.npv_default_leg(discount_curve, credit_curve) - \
                        self.npv_premium_leg(discount_curve, credit_curve)
        
        def breakevenRate(self, discount_curve, credit_curve):
                num = self.npv_default_leg(discount_curve, credit_curve)
                den = self.npv_premium_leg(discount_curve, credit_curve)/self.fixed_spread
                return num/den


