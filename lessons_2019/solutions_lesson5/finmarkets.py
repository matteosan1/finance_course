import math
import numpy
import scipy.stats

from datetime import date
from dateutil.relativedelta import relativedelta

def generate_swap_dates(start_date, n_months):
    
    dates = []
    for i in range(0, n_months, 12):
        dates.append(start_date + relativedelta(months=i))
    dates.append(start_date + relativedelta(months=n_months))
    
    return dates


class DiscountCurve:
    def __init__(self, today, pillar_dates, discount_factors):
        self.today = today
        self.log_discount_factors = [math.log(discount_factor) 
                                     for discount_factor in discount_factors]
        self.pillar_days = [(pillar_date - self.today).days for pillar_date in pillar_dates]

    def df(self, d):
        d_days = (d - self.today).days
        interpolated_log_discount_factor = numpy.interp(d_days, self.pillar_days, self.log_discount_factors)
        return math.exp(interpolated_log_discount_factor)

    def forward_libor(self, d1, d2):
        return (self.df(d1) / self.df(d2) - 1.0) * (365.0 / ((d2 - d1).days))

class OvernightIndexSwap(object):

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

