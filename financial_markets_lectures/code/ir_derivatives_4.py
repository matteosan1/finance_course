import pandas as pd

from datetime import date
from dateutil.relativedelta import relativedelta

from finmarkets import DiscountCurve, TermStructure, TimeInterval

obs_date = date.today()
discount_data = pd.read_excel('discount_factors_2022-10-05.xlsx')
euribor_data = pd.read_excel('euribor_curve.xlsx', sheet_name='EURIBOR6M')

dates = [obs_date + TimeInterval(i) for i in discount_data['maturities']]
dc = DiscountCurve(obs_date, dates, discount_data.loc[:, 'dfs'])

dates = [obs_date + TimeInterval(i) for i in euribor_data['maturities']]
fr = TermStructure(obs_date, dates, euribor_data.loc[:, 'rates']*0.01)

start_date = obs_date
exercise_date = start_date + TimeInterval("1Y")
nominal = 1e6
strike = 0.031
volatility = 0.15
swaption = InterestRateSwaption(nominal, start_date, exercise_date, "4y",\
                                volatility, strike, "6m")

price_bs = swaption.npv_Black(obs_date, dc, fr)
print (f"{price_bs:.2f}")
