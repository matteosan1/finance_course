from scipy.stats import norm

prob = norm.cdf(-5) * 2
nyears = 1/prob/365
print (nyears)