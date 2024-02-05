import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from finmarkets import generate_dates, CreditDefaultSwap, CreditCurve, DiscountCurve, saveObj
from scipy.optimize import minimize

obs_date = date.today()
cds_quotes = pd.read_excel('https://github.com/matteosan1/finance_course/raw/master/input_files/exercise_14.65.xlsx')
discount_data = pd.read_excel('https://github.com/matteosan1/finance_course/raw/master/input_files/discount_curve.xlsx')
dates = [obs_date + relativedelta(months=i) for i in discount_data['months']]
dc = DiscountCurve(obs_date, dates, discount_data.loc[:, 'dfs'])

cds_dates = []
creditdefaultswaps = []
for q in range(len(cds_quotes)):
    creditdefswap = CreditDefaultSwap(1, obs_date, 
                                      cds_quotes['maturity'].iloc[q], 
                                      cds_quotes['spread'].iloc[q])
    creditdefaultswaps.append(creditdefswap)
    cds_dates.append(creditdefswap.payment_dates[-1])
    
def obj_function(unknown_ndps, obs_date, cds_dates, dc):
    curve_c = CreditCurve(obs_date, cds_dates, unknown_ndps)
    sum_sq = 0.0
    for cds in creditdefaultswaps:
        sum_sq += cds.npv(dc, curve_c) ** 2
    return sum_sq

x0_guess = [0.001 for i in range(len(creditdefaultswaps))]
bounds_credit_curve = [(0.01, 1) for i in range(len(creditdefaultswaps))]
results = minimize(obj_function, x0_guess, bounds=bounds_credit_curve,
                   args=(obs_date, cds_dates, dc))
print (results.x)
credit_curve = CreditCurve(obs_date, cds_dates, results.x)
saveObj("credit_curve.pkl", credit_curve)
saveObj("discount_curve.pkl", dc)


from finmarkets import CreditDefaultSwap, CreditCurve, DiscountCurve, loadObj
from datetime import date

import pandas
from finmarkets import CreditDefaultSwap, CreditCurve, DiscountCurve, loadObj
from datetime import date

obs_date = date.today()
cds_to_price = pd.read_excel('https://github.com/matteosan1/finance_course/raw/master/input_files/exercise_14.66.xlsx')
cc = loadObj("credit_curve.pkl")
dc = loadObj("discount_curve.pkl")
npv_cds_to_price = []
for q in range(len(cds_to_price)):
    cds = CreditDefaultSwap(cds_to_price['nominal'].iloc[q], 
                            obs_date,
                            cds_to_price['maturity'].iloc[q], 
                            cds_to_price['spread'].iloc[q])
    npv_cds_to_price.append(cds.npv(dc, cc))
print (npv_cds_to_price)
