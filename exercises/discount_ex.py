import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

from finmarkets.finmarkets import DiscountCurve, ForwardRateCurve

def discount_factor(year):
    return 1/(1 + 0.1)**year

opt1 = {0:3000, 0.5:500, 1:500, 1.5:500, 2:500, 2.5:500, 3:500}
opt2 = {0:5000, 0.5:350, 1:350, 1.5:350, 2:350, 2.5:350, 3:350}
npv1 = sum([discount_factor(k)*v for k,v in opt1.items()])
npv2 = sum([discount_factor(k)*v for k,v in opt2.items()])
print ("Option1: {:.1f}".format(npv1))
print ("Option2: {:.1f}".format(npv2))

######################

def fv_factor(year):
    return (1 + 0.08)**year

fv = 0
for year in range(11):
    fv += 1000*fv_factor(year)
print ("future value: {:.1f}".format(fv))

######################
from datetime import date
from finmarkets import DiscountCurve
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/matteosan1/finance_course/develop/input_files/exercise_8.43.csv")
print (df.head())

obs_date = date.today()
df_dates = [obs_date + relativedelta(months=66),
            obs_date + relativedelta(months=126)]

num_dates = [(d.date()-obs_date).days for d in pd.to_datetime(df['dates'])]
target = (obs_date+relativedelta(months=18)-obs_date).days
print (np.interp(target, num_dates, df['yields']))

######################

dfs = []
dates = [d.date() for d in pd.to_datetime(df['dates'])]
for i, d in enumerate(dates):
    dfs.append(np.exp(-df['yields'][i]/100*((d-obs_date).days/365)))
dc = DiscountCurve(obs_date, dates[1:], dfs[1:])
print (dc.df(df_dates[0]))
print (dc.df(df_dates[1]))

######################
import pandas as pd
from finmarkets import ForwardRateCurve

from datetime import date
from dateutil.relativedelta import relativedelta

df = pd.read_csv("https://raw.githubusercontent.com/matteosan1/finance_course/master/input_files/exercise_8.43.csv")
obs_date = date.today()

fc = ForwardRateCurve(obs_date, dates, df['yields'])
print ("{:.4f}%".format(fc.forward_rate(obs_date + relativedelta(years=1),
                                        obs_date + relativedelta(years=11))/100))
