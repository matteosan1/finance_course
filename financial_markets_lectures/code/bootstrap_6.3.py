dc = DiscountCurve (today , pillars , np. concatenate (([1] , result .x )))
d = obs_date + TimeInterval ("40y")
print (f"40y df: {dc.df(d ):.3 f}")
print (f"40y rate : {dc. rate (d ):.4 f}")