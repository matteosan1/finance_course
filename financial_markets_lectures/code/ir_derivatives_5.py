pillars = TimeInterval("6y").generate_schedule(gc.OBS_DATE, "6m")
taus = np.array([yearFraction(gc.OBS_DATE, p, "ACT360") for p in pillars])
dfs = vasicek.P(r0, taus)
rates = vasicek.R(r0, taus)

discount_curve = DiscountCurve(pillars, dfs)
term_structure = TermStructure(pillars, rates)
swaption_price_black = swaption.npv_Black(volatility, 
                                          discount_curve, 
                                          term_structure)
print(f"Swaption Price Black: {swaption_price_black:,.2f} EUR")
