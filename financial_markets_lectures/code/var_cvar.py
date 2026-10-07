import numpy as np

from finmarkets import GlobalConst as gc
from finmarkets import TimeInterval, DiscountCurve, TermStructure, InterestRateSwap

np.random.seed(42)
risk_free_rate = 0.025

pillars = TimeInterval("6y").generate_schedule(obs_date, "1y")
dfs = (1+risk_free_rate)**-np.arange(0, 7)
dc = DiscountCurve(pillars, dfs)
libor = TermStructure([obs_date, obs_date + TimeInterval("6y")], [0.035, 0.035]) # flat Libor

swaps = []
swaps.append(InterestRateSwap(  1e6, start_date, "5Y", 0.03,   "1y", side="Payer"))
swaps.append(InterestRateSwap(  2e6, start_date, "5Y", 0.0285, "1y", side="Payer"))
swaps.append(InterestRateSwap(1.5e6, start_date, "5Y", 0.033,  "1y", side="Payer"))

portfolioNPV = sum([s.npv(dc, libor) for s in swaps])
print(f"NPV portfolio: {portfolioNPV:,.2f} EUR")

n_sims = 10000
PD = np.array([0.2, 0.5, 0.15])
R = 0.4
LGD = 1 - R

defaults = np.random.binomial(1, PD, size=(n_sims, 3))
exposures = np.array([max(s.npv(dc, libor), 0.0) for s in swaps])
losses = np.dot(defaults, exposures*LGD)

confidence_level = 0.95
credit_var = np.percentile(losses, confidence_level * 100)

n_defaults = np.sum(defaults, axis=1).astype(int)
counts = np.bincount(n_defaults, minlength=4)

print(f"Portfolio Credit VaR (at {int(confidence_level*100)}% c.l.) {credit_var:,.2f} EUR")