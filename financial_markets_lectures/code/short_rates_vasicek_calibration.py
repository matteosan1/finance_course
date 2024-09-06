import pandas as pd, numpy as np
import statsmodels.api as sm

df = pd.read_csv("TB3MS.csv")
df = df[df['DATE']>'2010-12-01']

df.dropna(inplace=True)
df['TB3MS'] = df['TB3MS']/100
df['prec'] = df['TB3MS'].shift(-1)

X = sm.add_constant(df['prec'][:-1])
y = df['TB3MS'][:-1]
model = sm.OLS(y, X)
r = model.fit()
print (r.summary())

dt = 1/12
theta = r.params['const']/(1-r.params['prec'])
k = (1-r.params['prec'])/dt
sigma = (np.sqrt(np.var(r.resid)))/dt
print (f"k: {k:.3f}, theta: {theta:.4f}, sigma: {sigma:.3f}")
