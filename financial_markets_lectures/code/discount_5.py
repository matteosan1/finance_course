from finmarkets import TermStructure, TimeInterval
from datetime import date

today = date.today()
pillars = [today + TimeInterval(i) for i in ['1y', '2y', '3y']]
spot_rates = [0.09, 0.095, 0.1]
ts = TermStructure(today, pillars, spot_rates)
t1 = today + TimeInterval('1y')
t2 = today + TimeInterval('2y')
t3 = today + TimeInterval('3y')

print (f"f_12 = {ts.forward_rate(t1, t2):.3f}")
print (f"f_23 = {ts.forward_rate(t2, t3):.3f}")
print (f"f_13 = {ts.forward_rate(t1, t3):.3f}")