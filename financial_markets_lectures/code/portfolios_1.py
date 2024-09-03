import pandas as pd, numpy as np

from scipy.optimize import minimize

df = pd.read_csv("portfolio_data.csv", index_col="date")
daily_returns = df.pct_change()
returns = daily_returns.mean()*252
covariance = daily_returns.cov()*252

def sum_weights(w): 
    return np.sum(w) - 1

def min_risk(w, cov):
    return w.T.dot(cov.dot(w))

def target_return(w, returns, target_return): 
    return (returns.dot(w) - target_return)

num_assets = 5
constraints = [{'type': 'eq', 'fun': sum_weights},
               {'type': 'eq', 'fun': target_return, 'args':(returns, 0.25)}] 
bounds = tuple((0, 1) for _ in range(num_assets))
weights = [1./num_assets for _ in range(num_assets)]

opts = minimize(min_risk, weights, args=(covariance,),
                bounds=bounds, constraints=constraints)
print (opts)
print (f"Expected portfolio return: {returns.dot(opts.x):.3f}")
