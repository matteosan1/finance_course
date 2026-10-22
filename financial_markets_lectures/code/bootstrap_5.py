from finmarkets import GlobalConst as gc, DiscountCurve, TimeInterval

d = gc.OBS_DATE + TimeInterval("40y")
print (f"40y df: {discount_curve.df(d):.3f}")
print (f"40y rate : {discount_curve.get_zero_rate(d):.4f}")