import pandas as pd

returns = pd.read_csv("capm.csv")
capm = CAPMModel(returns)
capm.fit('ret_GE', ['ret_Brent', 'ret_SP500'])
capm.fit('ret_XOM', ['ret_Brent', 'ret_SP500'])
