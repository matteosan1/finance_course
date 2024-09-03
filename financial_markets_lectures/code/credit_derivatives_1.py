from scipy.stats import binom

b = binom(100, 0.5) # params (n, p)
print (f"P(50): {b.pmf(50)*100:.2f}%")
