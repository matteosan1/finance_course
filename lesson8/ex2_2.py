from math import log, exp, sqrt
# You'll need the Gaussian cumulative distribution function
from scipy.stats import norm


def d1_m(m, r, vol, ttm):
    num = log(m) + (r + 0.5 * pow(vol, 2)) * ttm
    den = vol * sqrt(ttm)
    return num / den

def d2_m(m, r, vol, ttm):
    return d1_m(m, r, vol, ttm) - vol * sqrt(ttm)

def call_m(m, r, vol, ttm):
    return m * norm.cdf(d1_m(m, r, vol, ttm)) - norm.cdf(d2_m(m, r, vol, ttm))


def d1(S_t, K, r, vol, ttm):
    num = log(S_t/K) + (r + 0.5*pow(vol, 2)) * ttm
    den = vol * sqrt(ttm)
    if den == 0:
        return 100000000.
    return num/den

def d2(S_t, K, r, vol, ttm):
    return d1(S_t, K, r, vol, ttm) - vol * sqrt(ttm)

def call(S_t, K, r, vol, ttm):
    return S_t * norm.cdf(d1(S_t, K, r, vol, ttm)) - K * exp(-r * ttm) * norm.cdf(d2(S_t, K, r, vol, ttm))

def put(S_t, K, r, vol, ttm):
    return K * exp(-r * ttm) * norm.cdf(-d2(S_t, K, r, vol, ttm)) - S_t * norm.cdf(-d1(S_t, K, r, vol, ttm))

#S_t = 100.0
#ttm = 1
#K = 100.0
#vol = 0.25
#r = 0.01

#call_price = call(S_t, K, r, vol, ttm)
#put_price = put(S_t, K, r, vol, ttm)
#print ("{:.3f} {:.3f}".format(call_price, put_price))
