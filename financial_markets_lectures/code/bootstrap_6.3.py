from finmarkets import GlobalConst as gc, DiscountCurve, TimeInterval

dc = DiscountCurve (pillars , result.x)
d = gc.OBS_DATE + TimeInterval ("40y")
print (f"40y df: {dc.df(d ):.3 f}")
print (f"40y rate : {dc. rate (d ):.4 f}")