import pandas as pd, numpy as np

from scipy.stats import norm, t
from scipy.integrate import quad

df = pd.read_csv("historical_data.csv")
df['P'] = data.multiply(0.2, axis='columns').sum(axis=1)

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
print ("Gaussian")
print (f"1d-95% VaR: {var_continuous(f, 0.95):.4}")
print (f"1d-95% ES: {es_continuous(f, 0.95):.4}")

f2 = t.fit(df['P'])
model_t = t(*f2)

print ("t-student")
print (f"1d-95% VaR: {var_continuous(model_t, 0.95):.4f}")
print (f"1d-95% ES: {es_continuous(model_t, 0.95):.4f}")
