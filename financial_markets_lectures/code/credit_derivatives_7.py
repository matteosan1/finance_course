import numpy as np

from scipy.stats import binom, norm
from scipy.integrate import quad

N = 125
C = 1
R = 0
q = 0.02
tranches = [[1,3],[4, 6],[7,9]]

def p(M, rho, lims):
    qM = norm.cdf((norm.ppf(q)-np.sqrt(rho)*M)/(np.sqrt(1-rho)))
    pN = binom(N, qM)
    loss = 3*(pN.cdf(N) - pN.cdf(lims[1]-1))
    for i in range(lims[0], lims[1]):
        index = i-lims[0]+1
        loss += index*pN.pmf(i)
    return norm.pdf(M)*loss

res = [[],[],[]]
for i in range(len(tranches)):
    for rho in np.arange(0, 1.05, 0.05):
        if rho == 1.0:
            rho = 0.99
        v = quad(p, -np.inf, np.inf, args=(rho, tranches[i]))
        res[i].append(v[0])
