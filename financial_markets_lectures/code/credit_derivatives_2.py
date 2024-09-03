from scipy.stats import binom

b = binom(50, 0.085) # params (n, p)
prob = b.cdf(50)-b.cdf(4)s
print (f"P(>=5): {prob*100:.1f}%")