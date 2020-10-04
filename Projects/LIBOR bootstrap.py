#!/usr/bin/env python
# coding: utf-8

## In[76]:
#
#
##interpolation of OIS
#
#from datetime import date
#import numpy, math
#from matplotlib import pyplot as plt
#import matplotlib.dates as mdates
#import project6_data
#
## just some of the quotations from the list 
#today_date = date(2019, 10, 31)
#pillar_dates = [date(2019, 11, 12),date(2019, 11, 15),date(2019, 11, 18),date(2019, 11, 21)]
#discount_factors = [0.00138, 0.00152, 0.00166, 0.00184]
#
## the graph 
#plt.plot(pillar_dates, discount_factors, marker='o')
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
#plt.gca().xaxis.set_major_locator(mdates.YearLocator())
#plt.grid(True)
#plt.show()
#
#
#
#from datetime import date
#ois = OvernightIndexSwap(
#    # the notional
#    1e6,
#    # the start date and the list of product dates(just a part of them)
#[date(2019, 10, 31),
#date(2019, 12, 1),
#date(2019, 12, 2),
#date(2019, 12, 3),
#date(2019, 12, 4),
#date(2019, 12, 5),
#date(2019, 12, 6),
#date(2019, 12, 7),
#date(2019, 12, 8),
#date(2019, 12, 9),
#date(2019, 12, 10),
#date(2019, 12, 11),
#date(2019, 12, 12),
#date(2019, 12, 15),
#date(2019, 12, 18),
#date(2019, 12, 21),
#date(2019, 12, 24),
#date(2020, 1, 5),
#date(2020, 1, 17),
#date(2020, 1, 29)],
## the fixed rate,
#0.00351
#)
#
#
## In[14]:
#
#
#ois.npv(curve)
#
#
## In[18]:
#
#
#project6_data.today
#
#
## In[45]:
#
#
#ois = OvernightIndexSwap(1e6,
#
#[date(2019, 10, 31),#observation date
#date(2020, 5, 31),#180 days ??
#date(2020, 10, 31)],#last payment date
#project6_data.ois_quotes[12]['rate']*0.01
#)
#
## print the last payment date (12 months after obs date)
#ois.payment_dates[-1]
#
#
## In[46]:




from finmarkets import OvernightIndexSwap
from finmarkets import DiscountCurve, generate_swap_dates

import project6_data
pillar_dates = [project6_data.today]
swaps = []
# you are creating OIS so you need to loop over OIS inputs not IRS...
#for quote in project6_data.irs_quotes:
for quote in project6_data.ois_quotes:
    swap = OvernightIndexSwap(
        1e6,
        generate_swap_dates(
            project6_data.today,
            quote['maturity']
        ),
        # here you don't have to multiply by 0.00351
        # this the libor spot or the today value of the libor (today = 31/10/2019)
        quote['rate']
    )
    swaps.append(swap)
    pillar_dates.append(swap.payment_dates[-1])
    
pillar_dates = sorted(pillar_dates)
n_df_vector = len(pillar_dates)
print (pillar_dates)

def objective_function(x):
    curve = DiscountCurve(
        project6_data.today,
        pillar_dates,
        x
    )
    
    sum_sq = 0.0

    for swap in swaps:
        sum_sq += swap.npv(curve) ** 2
    return sum_sq


from scipy.optimize import minimize

x0 = [1.0 for i in range(n_df_vector)]
bounds = [(0.0001, 100.0) for i in range(n_df_vector)]
bounds[0] = (1.0, 1.0)
result = minimize(objective_function, x0, bounds=bounds)

print (result)
print(objective_function(x0))
print(objective_function(result.x))

# indeed the objective function before the bootstrap is very high
# after is very close to 0 meaning that you have found a discount curve
# that make reasonably good all the NPV of the OIS approximately 0...

curve = DiscountCurve(project6_data.today, pillar_dates, result.x)

# and this is correct, now you need to implement the rest to get the Libor Curve

