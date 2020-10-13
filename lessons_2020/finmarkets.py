import math, numpy

from datetime import date
from dateutil.relativedelta import relativedelta

def generate_swap_dates(start_date, n_months):
    """
    generate_swap_dates: computes a set of dates given starting date and length in months.
                         The tenor is by construction 12 months.

    Params:
    -------
    start_date: datetime.date
        The start date of the set of dates.
    n_months: int
        Number of months that define the length of the list of dates.
    """
    dates = []
    for i in range(0, n_months, 12):
        dates.append(start_date + relativedelta(months=i))
    dates.append(start_date + relativedelta(months=n_months))
    
    return dates

class DiscountCurve:
    """
    DiscountCurve: class that manage discount curves.

    Attributes:
    -----------
    today: datetime.date
        Observation date
    pillar_dates: list of datetime.date
        List of pillars of the discount curve.
    discount_factors: list of float
        List of the actual discount factors.
    """
    def __init__(self, today, pillar_dates, discount_factors):
        self.today = today
        self.pillar_dates = pillar_dates
        self.discount_factors = discount_factors
        
    def df(self, d):
        """
        df: method to get interpolated discoutn factor at `d`.

        Params:
        -------
        d: datetime.date
            The actual date at which we would like the interpolated discount factor.
        """
        log_discount_factors = \
            [math.log(discount_factor)
             for discount_factor in self.discount_factors]
        pillar_days = [(pillar_date - self.today).days
                       for pillar_date in self.pillar_dates]
        d_days = (d - self.today).days
        interpolated_log_discount_factor = \
            numpy.interp(d_days, pillar_days, log_discount_factors)
        return math.exp(interpolated_log_discount_factor)
    
    def forward_rate(self, d1, d2):
        """
        forward_rate: computes the forward rate referred to the period d2-d1.

        Params:
        -------
        d1: datetime.date
        d2: datetime.date
        """
        return (self.df(d1) / self.df(d2) - 1.0) * \
            (365.0 / ((d2 - d1).days))
    
class ForwardRateCurve(object):
    """
    ForwardRateCurve: container for a forward rate curve.

    Attributes:
    -----------
    pillar_dates: list of datetime.date
        List of pillars of the forward rate curve.
    pillar_rates: list of rates
        List of rates of the forward curve.
    """
    def __init__(self, pillar_dates, pillar_rates):
        self.today = pillar_dates[0]
        self.pillar_dates = pillar_dates
        self.pillar_rates = pillar_rates
        
        self.pillar_days = [
            (pillar_date - self.today).days
            for pillar_date in self.pillar_dates
        ]

    def forward_rate(self, d):
        """
        forward_rate: compute the forward rate at time d by interpolation.
        
        Params:
        -------
        d: datetime.date
            The date for the interpolation.
        """
        d_days = (d - self.today).days
        return numpy.interp(d_days, self.pillar_days, self.pillar_rates)

class OvernightIndexSwap:
    """
    OvernightIndexSwap: a class to valuate Overnight Index Swaps7.1. OVERNIGHT INDEX SWAP
    Attributes:
    -----------
    notional: float
        Notional of the swap.
    payment_dates: list of datetime.date
        List of payment dates of the swap.
    fixed_rate: float
        Rate of the fixed leg of the swap.
    """
    def __init__(self, notional, payment_dates, fixed_rate):
        self.notional = notional
        self.payment_dates = payment_dates
        self.fixed_rate = fixed_rate
        
    def npv_floating_leg(self, discount_curve):
        """
        npv_floating_leg: computes the floating leg npv.

        Params:
        -------
        discount_curve: DiscountCurve
            Discount curve object used for npv calculation.
        """
        return self.notional * (discount_curve.df(self.payment_dates[0]) -
                                discount_curve.df(self.payment_dates[-1]))

    def npv_fixed_leg(self, discount_curve):
        """
        npv_fixed_leg: computes the fixed leg npv.

        Params:
        -------
        discount_curve: DiscountCurve
            Discount curve object used for npv calculation.
        """
        npv = 0
        for i in range(1, len(self.payment_dates)):
            start_date = self.payment_dates[i-1]
            end_date = self.payment_dates[i]
            tau = (end_date - start_date).days / 360
            df = discount_curve.df(end_date)
            npv = npv + df * tau
        return self.notional * self.fixed_rate * npv
    
    def npv(self, discount_curve):
        """
        npv: computes the total npv of the swap.

        Params:
        -------
        discount_curve: DiscountCurve
            Discount curve object used for npv calculation.
        """
        float_npv = self.npv_floating_leg(discount_curve)
        fixed_npv = self.npv_fixed_leg(discount_curve)
        return float_npv - fixed_npv

    def fair_value_strike(self, discount_curve):
        """
        fair_value_strike: compute the fair value strike of the OIS.

        Params:
        -------
        discount_curve: DiscountCurve
            Discount curve object used for npv calculation.
        """
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
    
