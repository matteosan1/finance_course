import numpy as np

from finmarkets import generate_dates, CreditCurve
from scipy.stats import norm, binom
from scipy.integrate import quad

class CollDebtObligation:
    def __init__(self, nominal, N, tranches, rho, cc,
                 start_date, spreads, maturity, tenor="3m", recovery=0.4):
        self.nominal = nominal
        self.N = N
        self.tranches = tranches
        self.payment_dates = generate_dates(start_date, maturity, tenor)
        self.spreads = spreads
        self.rho = rho
        self.recovery = recovery
        self.cc = cc

    def one_factor_model(self, M, Q, l, L, U):
        P = norm.cdf((norm.ppf(Q) - np.sqrt(self.rho) * M) / (np.sqrt(1 - self.rho)))
        b = binom(self.N, P)
        return b.pmf(l) * norm.pdf(M) * max(min(l/self.N *
               self.nominal * (1 - self.recovery), U) - L, 0)

    def expected_tranche_loss(self, d, L, U):
        Q = 1 - self.cc.ndp(d)
        v = 0 
        for l in range(self.N+1):
            i = quad(self.one_factor_model, -np.inf, np.inf,
                args=(Q, l, L, U))[0]
            v += i
        return v

    def npv_premium(self, tranche, dc):
        L = self.tranches[tranche][0] * self.nominal
        U = self.tranches[tranche][1] * self.nominal
        v = 0
        for i in range(1, len(self.payment_dates)):
            ds = self.payment_dates[i - 1]
            de = self.payment_dates[i]
            D = dc.df(de)
            ETL = self.expected_tranche_loss(ds, L, U)
            v += D * (de - ds).days / 360 * max((U - L) - ETL, 0)
        return v * self.spreads[tranche]

    def npv_default(self, tranche, dc):
        U = self.tranches[tranche][1] * self.nominal
        L = self.tranches[tranche][0] * self.nominal
        v = 0
        for i in range(1, len(self.payment_dates)):
            ds = self.payment_dates[i - 1]
            de = self.payment_dates[i]
            ETL1 = self.expected_tranche_loss(ds, L, U)
            ETL2 = self.expected_tranche_loss(de, L, U)
            v += dc.df(de) * (ETL2 - ETL1)
        return v

    def npv(self, tranche, dc):
        return self.npv_default(tranche, dc) - self.npv_premium(tranche, dc)

    def fair_value(self, tranche, dc):
        num = self.npv_default(tranche, dc)
        den = self.npv_premium(tranche, dc) / self.spreads[tranche]
        return num / den