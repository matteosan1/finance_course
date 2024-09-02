import pandas as pd

from scipy.stats import t, multivariate_normal

data = pd.read_csv("bmw_siemens.csv", index_col='Date')
corr = data[['BMW.DE', 'SIE.DE']].corr()

bmw_fit_params = t.fit(bmw)
sie_fit_params = t.fit(sie)

f_bmw = t(*bmw_fit_params)
f_sie = t(df=sie_fit_params[0], loc=sie_fit_params[1], 
          scale=sie_fit_params[2])

N = 100000
mvnorm = multivariate_normal(mean=[0, 0], cov=corr)
x = mvnorm.rvs(N)
copula = norm.cdf(x)

bmw_corr = f_bmw.ppf(x_unif[:, 0])
sie_corr = f_sie.ppf(x_unif[:, 1])

bmw_uncorr = f_bmw.rvs(size=N)
sie_uncorr = f_sie.rvs(size=N)

def probability_down(N, sample1, sample2):
    n = 0
    for i in range(N):
        if bmw_corr[i] < 0.0 and sie_corr[i] < 0.0:
            n += 1
    return n/N

prob_corr = probability_down(N, bmw_corr, sie_corr)
prob_uncorr = probability_down(N, bmw_uncorr, sie_uncorr)
print (f"Probability w/ correlation: {prob_corr:.4f}")
print (f"Probability w/o correlation: {prob_uncorr:.4f}")