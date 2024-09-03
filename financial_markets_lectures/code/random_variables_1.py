from scipy.stats import norm

quantile = norm.ppf(0.3)
cdf = norm.cdf(quantile)
print (f"30%-quantile of standard normal is {quantile}")
print (f"CDF value at {quantile}: {cdf}")
