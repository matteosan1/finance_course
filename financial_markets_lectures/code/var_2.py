from numpy.random import choice
from numpy import percentile

def generate_returns(df, N=100000):
    data = df.reset_index()
    return data.loc[choice(range(len(data), N)]
    returns = df2['P'].loc[return_indexes]

def var_discrete(df, alpha=0.95):
    alpha = 1-alpha
    return -percentile(df, alpha*100)
    
def es_discrete(df, alpha=0.95):
    alpha = 1-alpha
    var = percentile(df, alpha*100)	
    return -df[df<=var].mean()
    
returns = generate_returns(df, 10000)
print (f"1d-95% VaR (discrete): {var_discrete(returns['P'], 0.95):.4f}")
print (f"1d-95% ES (discrete): {es_continuous(model, 0.95):.4f}")
