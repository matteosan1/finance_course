import matplotlib.pyplot as plt, numpy as np

from scipy.stats import multivariate_normal, multivariate_t

mean = np.array([bmw.mean(), sie.mean()])
cov = df[['BMW.DE', 'SIE.DE']].cov().values
bmw_std, sie_std = bmw.std(), sie.std()

rv_norm = multivariate_normal(mean, cov)
vals_norm = rv_norm.rvs(size=252 * 12)

nu = 4
shape_matrix = cov*(nu - 2)/nu
rv_t = multivariate_t(loc=mean, shape=shape_matrix, df=nu)
vals_t = rv_t.rvs(size=252 * 12)

l2 = rv_norm.pdf(mean + [2 * bmw_std, 2 * sie_std])
l5 = rv_norm.pdf(mean + [5 * bmw_std, 5 * sie_std])