results = []    
for target in np.arange(0.20, 0.45, 0.005):
    constraints = ({'type': 'eq', 'fun': sum_weights},
                   {'type': 'eq', 'fun': target_return,
                                  'args':(returns, target)})
    weights = [1./num_assets for _ in range(num_assets)]
    opts = minimize(min_risk, weights, args=(covariance,), 
                    bounds=bounds, constraints=constraints) 
    
    results.append((np.sqrt(opts.x.T.dot(covariance.dot(opts.x))),
                    returns.dot(opts.x))) 
