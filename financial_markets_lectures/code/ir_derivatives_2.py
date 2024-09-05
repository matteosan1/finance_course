import pandas as pd

from datetime import date
from finmarkets import DiscountCurve, TermStructure, TimeInterval

obs_date = date.today()
discount_data = pd.read_excel('discount_factors_2022-10-05.xlsx')
euribor_data = pd.read_excel('euribor_curve.xlsx', sheet_name='EURIBOR3M')

dates = [obs_date + TimeInterval(i) for i in discount_data['maturities']]
dc = DiscountCurve(obs_date, dates, discount_data.loc[:, 'dfs'])

dates = [obs_date + TimeInterval(i) for i in euribor_data['maturities']]
fr = TermStructure(obs_date, dates, euribor_data.loc[:, 'rates']*0.01)

start_date = obs_date + TimeInterval("1M")
nominal = 1e6
fixed_rate = 0.023
tenor = "3m"
maturity = "4y"

irs = InterestRateSwap(nominal, start_date, maturity, fixed_rate, tenor,\
                       side=SwapSide.Payer)
print ("{:.2f}".format(irs.npv(dc, fr)))
