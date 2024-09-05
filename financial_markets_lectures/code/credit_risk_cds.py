from finmarkets import generate_dates

class CreditDefaultSwap:
    def __init__(self, nominal, start_date, maturity, fixed_spread,
                 frequency="3m", recovery=0.4, side=SwapSide.Buyer):
        self.nominal = nominal
        self.payment_dates = generate_dates(start_date, maturity, frequency)
        self.fixed_spread = fixed_spread
        self.recovery = recovery
        self.side = side

    def npv_premium_leg(self, dc, cc):
        npv = 0
        for i in range(1, len(self.payment_dates)):
            tau = (self.payment_dates[i] - self.payment_dates[i-1]).days/365
            npv += dc.df(self.payment_dates[i])*\
                   cc.ndp(self.payment_dates[i]) * tau
        return self.fixed_spread * npv * self.nominal

    def npv_default_leg(self, dc, cc):
        npv = 0
        d = self.payment_dates[0]
        while d < self.payment_dates[-1]:
            npv += dc.df(d) * (
                   cc.ndp(d) -
                   cc.ndp(d + relativedelta(days=1)))
            d += relativedelta(days=1)
        return npv * self.nominal * (1 - self.recovery)

    def npv(self, dc, cc):
        return self.side*(self.npv_default_leg(dc, cc)-\
                          self.npv_premium_leg(dc, cc))

    def breakeven_rate(self, dc, cc):
        num = self.npv_default_leg(dc, cc)
        den = self.npv_premium_leg(dc, cc)/self.fixed_spread
        return num/den
