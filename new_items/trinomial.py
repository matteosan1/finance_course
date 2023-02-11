import numpy as np

def trinomial(optType, S, K, sigma, rfr, T, div, n):

    T1 = T / 365
    dt = T1 / n
    df = np.exp(-rfr * dt)
    cst = rfr - div

    if optType == "EC":
        optType = 1
    elif optType == "EP":
        optType = -1

    up = np.exp(sigma * np.sqrt(2 * dt))
    dn = np.exp(-sigma * np.sqrt(2 * dt))

    pUp = ((np.exp(cst * dt / 2) - np.exp(-sigma * np.sqrt(dt / 2))) / (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))) ** 2
    pDn = ((np.exp(sigma * np.sqrt(dt / 2)) - np.exp(cst * dt / 2)) / (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))) ** 2
    pStat = 1 - (pUp + pDn)

    val = np.zeros(shape=((n*2)+1,))
    for i in range(n*2):
        val[i] = max(0, optType * (S * up ** max(i - n, 0) * dn ** max(n * 2 - n - i, 0) - K))

    for x in range(n - 1, 0, -1):
        for i in range(x * 2):
            val[i] = (pUp * val[i + 2] + pStat * val[i + 1] + pDn * val[i]) * df

    return val

#optType, S, K, sigma, rfr, T, div, n):
print (trinomial("EC", 50, 50, 0.3, 0.05, 0.5, 0, 2))
