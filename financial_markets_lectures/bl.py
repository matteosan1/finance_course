import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
#import yfinance as yf

tickers = ['AMZN', 'BAC', 'COST', 'DIS', 'DPZ', 'KO', 'MCD', 'MSFT', 'NAT', 'SBUX']

# ohlc = yf.download(tickers, period="max")
# prices = ohlc["Adj Close"]
# prices.to_csv("bl_data.csv")
prices = pd.read_csv("bl_data.csv", index_col="Date")
returns = prices.pct_change()

#market_prices = yf.download("SPY", period="max")["Adj Close"]
#market_prices.to_csv("market.csv")
market_prices = pd.read_csv("market.csv", index_col="Date")

# mcaps = {}
# for t in tickers:
#     stock = yf.Ticker(t)
#     mcaps[t] = stock.info["marketCap"]
# with open("mkt_caps.json", "w") as f:
#     json.dump(mcaps, f)
with open("mkt_caps.json", "r") as f:
    market_caps = json.load(f)

from pypfopt import black_litterman, risk_models, BlackLittermanModel

frequency = 252
my_S = returns.cov().values * frequency
S = risk_models.sample_cov(prices)

risk_free_rate=0.02
delta = black_litterman.market_implied_risk_aversion(market_prices).values[0]
rets = market_prices.pct_change().dropna()
r = rets.mean().values[0] * frequency
var = rets.var().values[0] * frequency
my_delta = (r - risk_free_rate)/var

#plt.matshow(returns.corr())
#plt.show()

mcaps = pd.Series(market_caps)
mkt_weights = mcaps / mcaps.sum()
# Pi is excess returns so must add risk_free_rate to get return.
Pi = my_delta * my_S.dot(mkt_weights) + risk_free_rate

market_prior = black_litterman.market_implied_prior_returns(mcaps, delta, S)

#plt.bar(tickers, Pi)
#plt.show()

viewdict = {
    "AMZN": 0.10,
    "BAC": 0.30,
    "COST": 0.05,
    "DIS": 0.05,
    "DPZ": 0.20,
    "KO": -0.05,  # I think Coca-Cola will go down 5%
    "MCD": 0.15,
    "MSFT": 0.10,
    "NAT": 0.50,  # but low confidence, which will be reflected later
    "SBUX": 0.10
}

Q = np.array([[ 0.1 ],
 [ 0.3 ],
 [ 0.05],
 [ 0.05],
 [ 0.2 ],
 [-0.05],
 [ 0.15],
 [ 0.1 ],
 [ 0.5 ],
 [ 0.1 ]])
Q = np.array([0.1,0.3,0.05,0.05,0.2,-0.05,0.15,0.1,0.5,0.1])
P = np.identity(len(tickers))
intervals = [
    (0, 0.25),
    (0.1, 0.4),
    (-0.1, 0.15),
    (-0.05, 0.1),
    (0.15, 0.25),
    (-0.1, 0),
    (0.1, 0.2),
    (0.08, 0.12),
    (0.1, 0.9),
    (0, 0.3)
]

variances = []
for lb, ub in intervals:
    sigma = (ub - lb)/2
    variances.append(sigma ** 2)

omega = np.diag(variances)
tau = 0.05

tau_sigma_inv = np.linalg.inv(tau*my_S)
omega_inv = np.linalg.inv(omega)
p_omega_p = P.T.dot(omega_inv.dot(P))
# E_R = np.linalg.inv(tau_sigma_inv + p_omega_p)@((tau_sigma_inv.dot(Pi)) + P.T.dot(omega_inv.dot(Q)))

A = P.dot(tau*my_S.dot(P.T)) + omega
B = Q - P @ Pi
print (A.shape)
print (B.shape)
E_R_bis = Pi + tau*my_S.dot(P.T) @ np.linalg.solve(A, B)

bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict, omega=omega)

ret_bl = bl.bl_returns()

S_bl = bl.bl_cov()
my_S_new = my_S + np.linalg.inv(tau_sigma_inv + p_omega_p)

######################################################
# from pypfopt import EfficientFrontier, objective_functions
#
# ef = EfficientFrontier(ret_bl, S_bl)
# ef.max_sharpe()
# weights = ef.clean_weights()
# print (weights)


from scipy.optimize import minimize

num_assets = len(tickers)

def sum_weights(w):
    return np.sum(w) - 1

def my_sharpe_ratio(w, returns, rf_asset_return, cov):
    p_ret = returns.dot(w)
    p_var = np.sqrt(w.T.dot(cov.dot(w)))
    ratio = -(p_ret - rf_asset_return) / p_var
    return ratio

constraints = ({'type': 'eq', 'fun': sum_weights})
bounds = tuple((0, 1) for asset in range(num_assets))
weights = [1./num_assets for _ in range(num_assets)]
opts = minimize(my_sharpe_ratio, weights, args=(E_R_bis, risk_free_rate, my_S_new),
                bounds=bounds, constraints=constraints)
print (opts.x)

plt.pie(opts.x, labels=tickers)
plt.show()
