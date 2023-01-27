import numpy as np
from scipy.stats import norm

def d1(S, K, r, vol, ttm):
    num = np.log(S/K) + (r + 0.5*np.power(vol, 2)) * ttm
    den = vol * np.sqrt(ttm)
    return num/den

def d2(S, K, r, vol, ttm):
    return d1(S, K, r, vol, ttm) - vol*np.sqrt(ttm)

def call(S, K, r, vol, ttm):
    return (S * norm.cdf(d1(S, K, r, vol, ttm)) - \
           K*np.exp(-r*ttm)*norm.cdf(d2(S, K, r, vol, ttm)))

S = 800
# strikes expressed as % of spot price
moneyness = [0.5, 0.75, 0.825, 1.0, 1.125, 1.25, 1.5]
vol = 0.3
ttm = 0.75
r = 0.005

result = {}
for m in moneyness:
    result[S*m] = round(call(S, S*m, r, vol, ttm), 2)
print(result)
