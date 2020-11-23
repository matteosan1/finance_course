import quandl, pandas as pd, numpy as np, matplotlib.pyplot as plt

quandl.ApiConfig.api_key = 'LcdaEVsXUU2ZWG4ZysDs'
data = quandl.get_table('WIKI/PRICES', ticker=['AAPL', 'AMZN', 'BA', 'GOOG', 'IBM', 'MGM', 'T', 'TSLA'],
                        qopts={'columns': ['date', 'ticker', 'adj_close']},
                        date={'gte': '2013-12-30', 'lte': '2020-12-31'}, paginate=True)
data.to_csv("capm.csv", index=False)
