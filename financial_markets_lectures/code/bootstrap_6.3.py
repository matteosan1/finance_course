from dates import GlobalConsts as gc, TimeInterval
from curves import DiscountCurve

d = gc.OBS_DATE + TimeInterval ("40y")
print (f"40y df: {discount_curve.df(d):.3f}")
