from scipy.stats import norm
from math import sqrt

X = 0.999
rho = 0.1
R = 0.6
Q = 0.02
exposure = 100e6
num = norm.ppf(Q) + sqrt(rho)*norm.ppf(X)
den = sqrt(1-rho)
V = norm.cdf(num/den)
cr_var = exposure*V*(1-R)
