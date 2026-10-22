from scipy.stats import norm

quantile = norm.ppf(0.3)
cdf = norm.cdf(quantile)
print (f"30%-quantile of standard normal is {quantile:.4f}")
print (f"CDF value at {quantile:.4f}: {cdf:.4f}")
