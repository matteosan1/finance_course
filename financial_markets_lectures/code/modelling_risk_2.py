import pandas as pd

from scipy.stats import t, multivariate_normal

data = pd.read_csv("bmw_siemens.csv", index_col='Date')
corr = data[['BMW.DE', 'SIE.DE']].corr()
print (corr)

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

n_corr = np.sum((bmw_corr < 0) & (sie_corr < 0))
n_uncorr = np.sum((bmw_uncorr < 0) & (sie_uncorr < 0))

print (f"Probability w/ correlation: {n_corr/N:.4f}")
print (f"Probability w/o correlation: {n_uncorr/N:.4f}")