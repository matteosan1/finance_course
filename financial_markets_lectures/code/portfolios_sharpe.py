num_assets = 5
rf_asset_return = 0.10

def sharpe_ratio(w, returns, rf_asset_return, cov): 
    p_ret = returns.dot(w)
    p_var = np.sqrt(w.T.dot(cov.dot(w)))
    ratio = -(p_ret - rf_asset_return) / p_var
    return ratio

constraints = ({'type': 'eq', 'fun': sum_weights})
bounds = tuple((0, 1) for asset in range(num_assets))
weights = [1./num_assets for _ in range(num_assets)]
opts = minimize(sharpe_ratio, weights,
                args=(returns, rf_asset_return, covariance),
                bounds=bounds, constraints=constraints)
print (opts)
print ("Sharpe ratio: ", -opts.fun)
