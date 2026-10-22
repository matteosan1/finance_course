import numpy as np

from datetime import date
from dates import GlobalConsts as gc, TimeInterval, yearFraction
from curves import DiscountCurve, TermStructure
from ird import InterestRateSwap
from short_rate import VasicekModel

np.random.seed(42)
r0 = 0.02
a, b, sigma = 0.1, 0.03, 0.01

vasicek = VasicekModel(a, b, sigma)
swaption_exercise = TimeInterval("1y")
start_date_swap = gc.OBS_DATE + swaption_exercise
swap_tenor = "5y"
strike_K = 0.035
nominal = 1_000_000
float_freq = "6m"
N = 5000
volatility = 0.15

swap_m = InterestRateSwap(nominal=nominal, start_date=start_date_swap, 
                          maturity=swap_tenor, fixed_rate=strike_K, 
                          frequency_float=float_freq, side="Receiver")
swaption = Swaption(start_date=gc.OBS_DATE, 
                    exercise_date=start_date_swap, 
                    swap=swap_m)
swaption_price, cl = swaption.npv(N, r0, 1/12, vasicek)

print(f"Swaption Price: {swaption_price:,.2f} +- {cl:.2f} EUR")
