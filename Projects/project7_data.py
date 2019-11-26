from datetime import date

today = date(2019, 10, 31)

# par swap data
nominal = 100e6
libor_tenor = 6
fixed_leg_frequency = 12
maturity = 60

# CVA data
recovery = 0.40 
volatility = 0.30

ois_quotes = [
    {'maturity': 1, 'rate': 0.00106},
    {'maturity': 2, 'rate': 0.00114},
    {'maturity': 3, 'rate': 0.00115},
    {'maturity': 4, 'rate': 0.00117},
    {'maturity': 5, 'rate': 0.00119},
    {'maturity': 6, 'rate': 0.00121},
    {'maturity': 7, 'rate': 0.00122},
    {'maturity': 8, 'rate': 0.00124},
    {'maturity': 9, 'rate': 0.00128},
    {'maturity': 10, 'rate': 0.00131},
    {'maturity': 11, 'rate': 0.00135},
    {'maturity': 12, 'rate': 0.00138},
    {'maturity': 15, 'rate': 0.00152},
    {'maturity': 18, 'rate': 0.00166},
    {'maturity': 21, 'rate': 0.00184},
    {'maturity': 24, 'rate': 0.00206},
    {'maturity': 36, 'rate': 0.00344},
    {'maturity': 48, 'rate': 0.00543},
    {'maturity': 60, 'rate': 0.00756},
    {'maturity': 72, 'rate': 0.00967},
    {'maturity': 84, 'rate': 0.01162},
    {'maturity': 96, 'rate': 0.0134},
    {'maturity': 108, 'rate': 0.01502},
    {'maturity': 120, 'rate': 0.01649},
    {'maturity': 132, 'rate': 0.01776},
    {'maturity': 144, 'rate': 0.01888},
    {'maturity': 180, 'rate': 0.02137},
    {'maturity': 240, 'rate': 0.02322},
    {'maturity': 300, 'rate': 0.02389},
    {'maturity': 360, 'rate': 0.02416},
]

euribor_6m = [
    {'date': date(2019, 10, 31), 'rate': 0.005},
    {'date': date(2020, 4, 30), 'rate': 0.0058},
    {'date': date(2020, 10, 30), 'rate': 0.0066},
    {'date': date(2021, 4, 30), 'rate': 0.0074},
    {'date': date(2021, 10, 30), 'rate': 0.0082},
    {'date': date(2022, 4, 30), 'rate': 0.009},
    {'date': date(2022, 10, 30), 'rate': 0.0098},
    {'date': date(2023, 4, 30), 'rate': 0.0106},
    {'date': date(2023, 10, 30), 'rate': 0.0114},
    {'date': date(2024, 4, 30), 'rate': 0.0122},
    {'date': date(2024, 10, 30), 'rate': 0.013},
    {'date': date(2025, 4, 30), 'rate': 0.0138},
    {'date': date(2025, 10, 30), 'rate': 0.0146},
    {'date': date(2026, 4, 30), 'rate': 0.0154},
    {'date': date(2026, 10, 30), 'rate': 0.0162},
    {'date': date(2027, 4, 30), 'rate': 0.017},
    {'date': date(2027, 10, 30), 'rate': 0.0178},
    {'date': date(2028, 4, 30), 'rate': 0.0186},
    {'date': date(2028, 10, 30), 'rate': 0.0194},
    {'date': date(2029, 4, 30), 'rate': 0.0202},
    {'date': date(2029, 10, 30), 'rate': 0.021},
    {'date': date(2030, 4, 30), 'rate': 0.0218},
    {'date': date(2030, 10, 30), 'rate': 0.0226},
    {'date': date(2031, 4, 30), 'rate': 0.0234},
    {'date': date(2031, 10, 30), 'rate': 0.0242},
    {'date': date(2032, 4, 30), 'rate': 0.025},
    {'date': date(2032, 10, 30), 'rate': 0.0258},
    {'date': date(2033, 4, 30), 'rate': 0.0266},
    {'date': date(2033, 10, 30), 'rate': 0.0274},
    {'date': date(2034, 4, 30), 'rate': 0.0282},
]

survival_probabilities = [
    {'date': date(2020, 12, 20), 'ndp': 0.972159727015014},
    {'date': date(2021, 12, 20), 'ndp': 0.942926329174406},
    {'date': date(2022, 12, 20), 'ndp': 0.913448056250137},
    {'date': date(2024, 12, 20), 'ndp': 0.855640452819766},
    {'date': date(2029, 12, 20), 'ndp': 0.732687779675469},
    {'date': date(2039, 12, 20), 'ndp': 0.539046016487758},
]