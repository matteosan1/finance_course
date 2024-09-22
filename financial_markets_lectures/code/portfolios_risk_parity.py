num_assets = 5
def risk_parity(w, cov):
    variance = w.T.dot(cov.dot(w))
    *@sum@* = 0
    N = len(w)
    for i in range(N):
        *@sum@* += (w[i] - (variance/(N*cov.dot(w)[i])))**2
    return *@sum@*
	
args = (covariance,)
constraints = ({'type': 'eq', 'fun': sum_weights})
bounds = tuple((0, 1) for asset in range(num_assets))
weights = [1./num_assets for _ in range(num_assets)]
opts = minimize(risk_parity, weights, args=(covariance,),
                bounds=bounds, constraints=constraints)

sigma_i = []
std = np.sqrt(opts.x.T.dot(covariance.dot(opts.x)))
for i in range(num_assets):
    a = opts.x[i]*covariance.dot(opts.x)[i]
	sigma_i.append(a/std)

print (opts)
	
for i in range(num_assets):
    print (f"Risk per asset {i}: {sigma_i[i]/sum(sigma_i)*100:.3f}%")

