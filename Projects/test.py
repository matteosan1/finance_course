from finmarkets import InterestRateSwap
from curve_data import discount_curve, libor_curve

from datetime import date

pricing_date = date(2019,11,23)
irs = InterestRateSwap(pricing_date, 1e6, 0.05, 6, 4)
print (irs.npv(discount_curve, libor_curve))

print (irs.swap_rate(discount_curve, libor_curve))

print (irs.spread(discount_curve, libor_curve))
