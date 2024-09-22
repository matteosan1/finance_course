num_assets = 6
returns_rf = np.append(returns.values, 0.10)
cov_rf = np.zeros(shape=(num_assets, num_assets))
cov_rf[:num_assets-1, :num_assets-1] = covariances.values

result_rf = []

for t_ret in np.arange(0.1, 0.4, 0.01):
    weights = [1/n_assets for _ in range(num_assets)]
    bounds = [(0, 1) for _ in range(num_assets)]
    constraints = [{'type':'eq', 'fun':sum_weights},
                   {'type':'eq', 'fun':target_return,
                                 'args':(returns_rf, t_ret)}]

    opts = minimize(min_risk, weights, bounds=bounds, 
                    constraints=constraints, args=(cov_rf))

    result_rf.append((np.sqrt(risk(opts.x, covariance)),
                      returns.dot(opts.x)))
