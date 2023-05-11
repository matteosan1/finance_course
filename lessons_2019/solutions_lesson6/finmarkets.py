import math
import numpy

from dateutil.relativedelta import relativedelta

# Discount curve class
class DiscountCurve(object):
    
    # the special __init__ method defines how to
    # construct instances of the class
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
        
        
    # calculates a discount factor at an arbitrary value
    # date using the data stored in the instance
    def df(self, d):
        
        # these remain local variables, i.e. they are only
        # available within the function to read (or write) instance
        # attributes, you always need to use the self. syntax
        
        d_days = (d - self.today).days
        
        interpolated_log_discount_factor = numpy.interp(d_days, self.pillar_days, self.log_discount_factors)
        
        return math.exp(interpolated_log_discount_factor) 
    
    
    # calculates a forward libor rate based on the discount
    # curve data stored in the instance
    def forward_libor(self, d1, d2):
       
        # we use the df method of the current instance to
        # calculate the forward rate
        return (
            self.df(d1) /
            self.df(d2) - 1
        ) / ((d2  - d1).days / 365)
    

class OvernightIndexSwap(object):
    
    # this method is called to build the instance, we take some
    # data arguments and save them as attributes of self
    # n.b.: payment_dates should be a list of dates, including
    # the start date as the first element
    def __init__(self, notional, payment_dates, fixed_rate):
        
        self.notional = notional
        self.payment_dates = payment_dates
        self.fixed_rate = fixed_rate
        
    # this method takes a discount curve and calculates the NPV
    # of the floating leg using that curve
    def npv_floating_leg(self, discount_curve):
        
        return self.notional * (
            # self.payment_dates[0] is the start date of the swap
            discount_curve.df(self.payment_dates[0]) - 
            
            # self.payment_dates[-1] is the last payment date of the swap
            discount_curve.df(self.payment_dates[-1])      
        )
    
    # this method takes a discount curve and calculates the NPV of
    # the fixed leg using that curve
    def npv_fixed_leg(self, discount_curve):
        
        npv = 0
        
        # we loop from i=1 up to but not including the length of
        # the date list
        for i in range(1, len(self.payment_dates)):   
            
            start_date = self.payment_dates[i-1]
            # we can do i-1, because the loop starts with i=1
            
            end_date = self.payment_dates[i]
            
            tau = (end_date - start_date).days / 360
            df = discount_curve.df(end_date)
            
            npv = npv + df * tau
            
        return self.notional * self.fixed_rate * npv
    
    # this method calculates the NPV of the OIS swap
    # n.b.: inside this method we call the other two methods of
    #       the class on the same instance 'self', using
    #       self.npv_XXX_leg(...), and we pass the discount_curve
    #       we received as an argument
    def npv(self, discount_curve):
        
        float_npv = self.npv_floating_leg(discount_curve)
        fixed_npv = self.npv_fixed_leg(discount_curve)
        
        return float_npv - fixed_npv
    
    
def generate_swap_dates(start_date, n_months, tenor_months=12):
    
    dates = []
    
    for n in range(0, n_months, tenor_months):
        dates.append(start_date + relativedelta(months=n))
    dates.append(start_date + relativedelta(months=n_months))
    
    return dates    


# an EURIBOR or LIBOR rate curve
# doesn't calculate discount factors, only interpolates forward rates
class ForwardRateCurve(object):
    
    # the special __init__ method defines how to
    # construct instances of the class
    def __init__(self, pillar_dates, pillar_rates):
        
        # we just store the arguments as attributes of the instance
        self.today = pillar_dates[0]
        self.pillar_dates = pillar_dates
        self.pillar_rates = pillar_rates
        
        self.pillar_days = [
            (pillar_date - self.today).days
            for pillar_date in self.pillar_dates
        ]
        
        
    # interpolates the forward rates stored in the instance
    def forward_rate(self, d):
       
        d_days = (d - self.today).days
        
        return numpy.interp(d_days, self.pillar_days, self.pillar_rates)


from finmarkets import generate_swap_dates

class InterestRateSwap:
    
    def __init__(self, start_date, notional, fixed_rate, tenor_months, maturity_years):
        self.notional = notional
        self.fixed_rate = fixed_rate
        self.fixed_leg_dates = generate_swap_dates(start_date, 12 * maturity_years)
        self.floating_leg_dates = generate_swap_dates(start_date, 12 * maturity_years,
                                                      tenor_months)
        
    def annuity(self, discount_curve):
        a = 0
        for i in range(1, len(self.fixed_leg_dates)):
            a += discount_curve.df(self.fixed_leg_dates[i])
        return a

    def swap_rate(self, discount_curve, libor_curve):
        s = 0
        for j in range(1, len(self.floating_leg_dates)):
            F = libor_curve.forward_rate(self.floating_leg_dates[j-1])
            tau = (self.floating_leg_dates[j] - self.floating_leg_dates[j-1]).days / 360
            P = discount_curve.df(self.floating_leg_dates[j])
            s += F * tau * P
        return s / self.annuity(discount_curve)
        
    def npv(self, discount_curve, libor_curve):
        S = self.swap_rate(discount_curve, libor_curve)
        A = self.annuity(discount_curve)
        return self.notional * (S - self.fixed_rate) * A
