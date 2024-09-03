import pandas as pd, numpy as np

from scipy.stats import norm, t
from scipy.integrate import quad

df = pd.read_csv("historical_data.csv", index_col='Date')
df['P'] = df['aapl']*0.6 + df['nflx']*0.4
df = df.pct_change()
df.dropna(inplace=True)

mu = df.mean() 
sigma = df.std()

def var_continuous(f, alpha=0.95):
    return -f.ppf(1-alpha)

def es_continuous(f, alpha=0.95):
  def integrand(x, f):
    return f.ppf(x)

  alpha = 1-alpha
  I = quad(integrand, 0, alpha, args=(f,))
  return -1/alpha*I[0]
    
f = norm(mu['P'], sigma['P'])
print (f"1d-95% VaR: {var_continuous(f, 0.95):.4}")
print (f"1d-95% ES: {es_continuous(f, 0.95):.4}")

f2 = t.fit(df['P'])
model_t = t(*f2)

print (f"1d-95% VaR: {var_continuous(model_t, 0.95):.4f}")
print (f"1d-95% ES: {es_continuous(model_t, 0.95):.4f}")