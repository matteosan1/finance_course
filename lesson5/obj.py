from finmarkets import DiscountCurve, generate_swap_dates
import ois_data_eric as ois_data
from scipy.optimize import minimize
import numpy as np

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

class OvernightIndexSwap2(object):
    
    # this method is called to build the instance, we take some data arguments and save them as attributes of self
    # n.b.: payment_dates should be a list of dates, including the start date as the first element
    def __init__(self, notional, payment_dates, fixed_rate):
        
        self.notional = notional
        self.payment_dates = payment_dates
        self.fixed_rate = fixed_rate
        
    # this method takes a discount curve and calculates the NPV of the floating leg using that curve
    def npv_floating_leg(self, discount_curve):
        
        return self.notional * (
            discount_curve.df(self.payment_dates[0]) -     # self.payment_dates[0] is the start date of the swap
            discount_curve.df(self.payment_dates[-1])      # self.payment_dates[-1] is the last payment date of the swap
        )
    
    # this method takes a discount curve and calculates the NPV of the fixed leg using that curve
    def npv_fixed_leg(self, discount_curve):
        
        npv = 0
        
        for i in range(1, len(self.payment_dates)):   # we loop from i=1 up to but not including the length of the date list
            
            start_date = self.payment_dates[i-1]    # we can do i-1, because the loop starts with i=1
            end_date = self.payment_dates[i]
            
            tau = (end_date - start_date).days / 360
            df = discount_curve.df(end_date)
            
            npv = npv + df * tau
            
        return self.notional * self.fixed_rate * npv
    def npv(self, discount_curve):
        
        float_npv = self.npv_floating_leg(discount_curve)
        fixed_npv = self.npv_fixed_leg(discount_curve)        
        return float_npv - fixed_npv
            
    
pillar_dates = [ois_data.observation_date]

swaps = [] # container of the OIS objects

for quote in ois_data.quotes:
    swap = OvernightIndexSwap(
        1e6,
        generate_swap_dates(
            ois_data.observation_date,
            quote['months']
        ),
        0.01 * quote['rate']
    )
    swaps.append(swap)
    pillar_dates.append(swap.payment_dates[-1])
    
pillar_dates = sorted(pillar_dates)
n_df_vector = len(pillar_dates)
#print (pillar_dates, n_df_vector)
def objective_function(x):    
    curve = DiscountCurve(       
        ois_data.observation_date,
        pillar_dates,
        x
    )
    
    sum_sq = 0.0
    for swap in swaps:
        sum_sq += swap.npv(curve) ** 2        
    return sum_sq


from datetime import date
curve = DiscountCurve(date(2020, 1, 1),
                      [date(2020, 1, 1), 
                       date(2021, 6, 1), 
                       date(2022, 1, 1)],
                      [1.0, 0.98, 0.82])
print (curve.df(date(2020, 7, 1)))
ois = OvernightIndexSwap(
    # the notional, one million
    1e6,
    # the list of product dates, 
    # i.e. the start date then the payment dates
    [date(2020, 1, 1), 
     date(2020, 4, 1), 
     date(2020, 7, 1), 
     date(2020, 10, 1),
     date(2021, 1, 1)],
    # the fixed rate, 2.5%
    0.025
)
#ois = OvernightIndexSwap(1e6,
#                         [date(2019, 10, 23), 
#                          date(2020, 10, 23), 
#                          date(2020, 1, 23)],                        
#                         ois_data.quotes[12]['rate']*0.01 
#)
#
ois2 = OvernightIndexSwap2(
    1e6,
    [
        date(2016, 1, 1),
        date(2016, 4, 1),
        date(2016, 7, 1),
        date(2016, 10, 1),
        date(2017, 1, 1),
    ],
    0.025   
)
print (ois.payment_dates[-1])
print (ois.npv(curve))
#print (ois2.npv(curve))
#import sys
#sys.exit()

x0 = [1.0 for i in range(n_df_vector)] 
bounds = [(0.01, 100.0) for i in range(n_df_vector)] 
bounds[0] = (1.0, 1.0)

of = []
def p(x0):
    of.append(objective_function(x0))

result = minimize(objective_function, x0, bounds=bounds, callback=p)
print (pillar_dates)
print (len(swaps))
print (result)

from matplotlib import pyplot as plt
plt.rc('text', usetex=True)
xc=[]
zc=[]
for x1 in range(-100, 100):
    x1_coord = result.x[1]+x1/1000000
    xn = [1.0, x1_coord] + result.x.tolist()[2:]
    xc.append(x1_coord)
    zc.append(objective_function(xn))

plt.plot(xc, zc)
plt.xlabel(r'discount factor ($x_{1}$)')
plt.ylabel("objective function value")
plt.plot(result.x[1], objective_function(result.x), marker='o')
plt.savefig("obj_func.png")

#plt.plot(range(12), of)
#plt.ylabel("objective function value")
#plt.xticks(np.arange(12), ["iter"+str(i) for i in range(1, 13)])
#plt.yscale("log")
#plt.savefig("obj_func_iter.png")
#
