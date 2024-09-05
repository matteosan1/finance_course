import numpy as np

np.random.seed(1)
swaption = InterestRateSwaption(nominal, start_date, exercise_date, "4y",\
                                volatility, strike, "6m")

price_mc, interval = swaption.npv_MC(obs_date, dc, fr)
print (f"MC: {price_mc:.2f} +- {interval:.2f}")

price_bs = swaption.npv_Black(obs_date, dc, fr)
print (f"BS: {price_bs:.2f}")
