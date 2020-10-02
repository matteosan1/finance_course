import quandl, pandas as pd, numpy as np, matplotlib.pyplot as plt, scipy.optimize as sco

from os.path import isfile

class MarkowitzOptimization:

    def __init__(self, selected=None, df=None):
        self.df = df
        self.selected = selected

    def getDataFromQuandl(self, selected):
        self.selected = selected

        if not isfile('quandl.csv'):
            quandl.ApiConfig.api_key = 'LcdaEVsXUU2ZWG4ZysDs'
            data = quandl.get_table('WIKI/PRICES', ticker=selected,
                                    qopts={'columns': ['date', 'ticker', 'adj_close']},
                                    date={'gte': '2014-1-1', 'lte': '2019-12-31'}, paginate=True)
            data.to_csv("quandl.csv", index=False)
            clean = data.set_index('date')
            self.df = clean.pivot(columns='ticker')
        else:
            temp = pd.read_csv("quandl.csv")
            clean = temp.set_index('date')
            self.df = clean.pivot(columns='ticker')

    def dailyReturns(self):
        return self.df.pct_change()

    def dailyCovariance(self):
        return self.dailyReturns().cov()

    def annualReturns(self):
        return self.dailyReturns().mean() * 252

    def annualCovariance(self):
        return self.dailyCovariance() * 252

    def mcSimulation(self):
        port_returns = []
        port_volatility = []
        stock_weights = []
        ratios = []

        annual_returns = self.annualReturns()
        annual_covariance = self.annualCovariance()

        num_assets = len(self.selected)
        num_portfolios = 50000

        for single_portfolio in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            returns = np.dot(weights, annual_returns)
            volatility = np.sqrt(np.dot(weights.T, np.dot(annual_covariance, weights)))
            port_returns.append(returns)
            port_volatility.append(volatility)
            stock_weights.append(weights)
            #ratios.append(self.sharpeRatio(weights, 0.01))

        #plt.hist(ratios)
        #plt.show()

        portfolio = {'Returns': port_returns, 'Volatility': port_volatility}
        for counter,symbol in enumerate(self.selected):
            portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]

        df = pd.DataFrame(portfolio)
        column_order = ['Returns', 'Volatility'] + [stock+' Weight' for stock in self.selected]
        df = df[column_order]

        plt.style.use('seaborn')
        df.plot.scatter(x='Volatility', y='Returns', figsize=(10, 8), color="lightgray",
                        grid=True, label="MC Simulated Portfolios")
        plt.xlabel('Volatility (Std. Deviation)')
        plt.ylabel('Expected Returns')
        plt.title('Efficient Frontier')
        return plt

    def portfolioPerformance(self, weights):
        meanReturns = self.annualReturns()
        portReturn = np.sum(meanReturns * weights)
        portStdDev = np.sqrt(np.dot(weights.T, np.dot(self.annualCovariance(), weights)))

        return portReturn, portStdDev

    def sharpeRatio(self, weights, riskFreeRate):
        p_ret, p_var = self.portfolioPerformance(weights)
        ratio = -(p_ret - riskFreeRate) / p_var
        return ratio

    def getPortfolioReturn(self, weights):
        return self.portfolioPerformance(weights)[0]

    def getPortfolioVol(self, weights):
        return self.portfolioPerformance(weights)[1]

    def findMaxSharpeRatioPortfolio(self, riskFreeRate):
        numAssets = len(self.selected)
        args = (riskFreeRate,)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},)
        bounds = tuple((0, 1)   for asset in range(numAssets))

        opts = sco.minimize(self.sharpeRatio, np.ones(numAssets) / float(numAssets), args=args,
                            method='SLSQP', bounds=bounds, constraints=constraints)
        return opts

    def findMinVariancePortfolio(self):
        numAssets = len(self.selected)
        args = ()
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},)
        bounds = tuple((0, 1) for asset in range(numAssets))

        opts = sco.minimize(self.getPortfolioVol, np.ones(numAssets) / float(numAssets), args=args,
                            method='SLSQP', bounds=bounds, constraints=constraints)

        return opts

    def findEfficientReturn(self, targetReturn):
        numAssets = len(self.selected)
        args = ()

        constraints = ({'type': 'eq', 'fun': lambda x: self.getPortfolioReturn(x) - targetReturn},
                       {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for asset in range(numAssets))

        return sco.minimize(self.getPortfolioVol, np.ones(numAssets) / float(numAssets), args=args,
                            method='SLSQP', bounds=bounds, constraints=constraints)

    def findEfficientFrontier(self, rangeOfReturns):
        efficientPortfolios = []
        for ret in rangeOfReturns:
            efficientPortfolios.append(self.findEfficientReturn(ret))

        return efficientPortfolios

markow = MarkowitzOptimization()
markow.getDataFromQuandl(['CNP', 'F', 'WMT', 'GE', 'TSLA'])
markow.mcSimulation()

maxSharpe = markow.findMaxSharpeRatioPortfolio(0.0001)
rp, sdp = markow.portfolioPerformance(maxSharpe['x'])
print (rp, sdp)
plt.scatter(sdp, rp, marker="*", s=70, color="blue", label="Max Sharpe Ratio Portfolio")

# Find portfolio with minimum variance
minVar = markow.findMinVariancePortfolio()
rp, sdp = markow.portfolioPerformance(minVar['x'])
print (rp, sdp)
plt.scatter(sdp, rp, marker="x", color="green", s=50, label="Min Volatility Portfolio")

# Find efficient frontier, annual target returns of 9% and 16%
targetReturns = np.linspace(0.02, 0.16, 50)
efficientPortfolios = markow.findEfficientFrontier(targetReturns)
frontier = []
for eff in efficientPortfolios:
    perf = markow.portfolioPerformance(eff['x'])
    print (perf)
    frontier.append(perf)

frontier = np.array(frontier)
plt.plot(frontier[:, 1], frontier[:, 0], color="red", linestyle="--", label="Efficiency Frontier")
plt.legend()
plt.show()