import pandas as pd
from scipy.stats import norm

spy = pd.read_csv('SPX.csv', index_col="Date") 
spy.index = pd.to_datetime(spy.index)

spy['pct_change'] = spy['Close'].pct_change()
spy.dropna(inplace=True) 

train = spy['2009':'2015']
test = spy['2016':]

print (train.index.min(), train.index.max(), test.index.min(), test.index.max())

train_returns = train['pct_change']
params = norm.fit(train_returns)
x = np.arange(-0.06, 0.06, 0.001)

plt.hist(train_returns, bins=50, density=True)
plt.plot(x, norm(*params).pdf(x))
plt.show()