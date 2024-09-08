import statsmodels.api as sm, pandas as pd

capm = pd.read_csv("capm.csv")
X = capm['ret_SP500']
y = capm['ret_GE']
	
X = sm.add_constant(X)
est = sm.OLS(y, X).fit()
print(est.summary())
