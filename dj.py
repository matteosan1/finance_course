#tickers = ["BA","CAT","CVX",
#"CSCO","KO",
#"DOW","XOM",
#"GS","HD",
#"INTC","IBM",
#"JNJ","JPM",
#"MCD","MRK",
#"MSFT","NKE",
#"PFE","PG",
#"RTX","TRV",
#"UNH","VZ",
#"V","WBA", "WMT", "^DJI"]
#
#import ffn
#returns = ffn.get(tickers, start='2009-01-01').to_returns().dropna()
#returns.to_csv("prova.csv")

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.dates import MonthLocator
import matplotlib.dates as mdates

df_start = pd.read_csv("prova.csv", index_col='Date')
df = df_start.iloc[:, :-1]

cov = df.cov()
eigVals, eigVecs = np.linalg.eig(cov)
indices = [i for i in reversed(np.argsort(eigVals))]

l = [eigVals[i]/np.sum(eigVals) for i in reversed(np.argsort(eigVals))]
#plt.bar(range(26), l)
#plt.show()

norm_eigVecs = [v/np.linalg.norm(v) for v in eigVecs.T]

index = indices[0]
#plt.bar(range(26), norm_eigVecs[index])
#plt.show()

df['pca1'] = df.dot(norm_eigVecs[index])

plt.figure(figsize=(12, 6))
sub1 = plt.subplot(1,2,1)
sub1.plot(df['pca1'].cumsum(), label="PCA1")
sub1.xaxis.set_major_locator(MonthLocator(interval=2))
sub1.tick_params('x', labelrotation=45, labelsize=8)
sub1.legend()

sub2 = plt.subplot(1,2,2)
sub2.plot(df_start['dji'].cumsum(), color='green', label="DJI")
sub2.xaxis.set_major_locator(MonthLocator(interval=2))
sub2.tick_params('x', labelrotation=45, labelsize=8)
sub2.legend()

plt.show()
