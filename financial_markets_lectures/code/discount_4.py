from dates import GlobalConsts as gc, TimeInterval
from curves import TermStructure

t0 = gc.OBS_DATE
spot_rates = [0.09, 0.095, 0.10]
t1 = gc.OBS_DATE + TimeInterval('1Y')
t2 = gc.OBS_DATE + TimeInterval('2Y')
t3 = gc.OBS_DATE + TimeInterval('3Y')

pillars = [t1, t2, t3]

ts = TermStructure(pillars, spot_rates)
print (f"F(t1, t2; t0) = {ts.forward_rate(t1, t2)}")
print (f"F(t2, t3; t0) = {ts.forward_rate(t2, t3)}")
print (f"F(t1, t3; t0) = {ts.forward_rate(t1, t3):0.3f}")
