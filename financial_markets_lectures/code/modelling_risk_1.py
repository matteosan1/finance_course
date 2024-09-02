from scipy.stats import uniform, norm

x = uniform(0, 1).rvs(10000)
x_trans = norm.ppf(x)
x_clone = norm.cdf(x_trans)