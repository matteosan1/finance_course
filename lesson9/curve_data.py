from finmarkets import DiscountCurve, ForwardRateCurve
from datetime import date

discount_curve = DiscountCurve(
    pricing_date,
    [
        date(2019, 11, 23),
        date(2019, 12, 23),
        date(2020, 1, 23),
        date(2020, 2, 23),
        date(2020, 3, 23),
        date(2020, 4, 23),
        date(2020, 5, 23),
        date(2020, 6, 23),
        date(2020, 7, 23),
        date(2020, 8, 23),
        date(2020, 9, 23),
        date(2020, 10, 23),
        date(2020, 11, 23),
        date(2021, 2, 23),
        date(2021, 5, 23),
        date(2021, 8, 23),
        date(2021, 11, 23),
        date(2022, 11, 23),
        date(2023, 11, 23),
        date(2024, 11, 23),
        date(2025, 11, 23),
        date(2026, 11, 23),
        date(2027, 11, 23),
        date(2028, 11, 23),
        date(2029, 11, 23),
        date(2030, 11, 23),
        date(2031, 11, 23),
        date(2034, 11, 23),
        date(2037, 11, 23),
        date(2044, 11, 23),
        date(2049, 11, 23),
        date(2059, 11, 23),
        date(2069, 11, 23),
        date(2079, 11, 23)
    ],
    [
        1.0,
        1.0002917467402148,
        1.0005883131272417,
        1.0008901199538236,
        1.0011680243827714,
        1.0014702089411212,
        1.001767864893772,
        1.0020712764009907,
        1.0023650754871887,
        1.0026688489207509,
        1.0029728065322525,
        1.0032577961650622,
        1.0035612434176608,
        1.0044596767629976,
        1.0052998330195502,
        1.0061426892578045,
        1.0069306074274715,
        1.0090620121240119,
        1.0093198010276425,
        1.0071011202467379,
        1.001898602291577,
        0.99379503923610302,
        0.98332969774581891,
        0.97101000579044472,
        0.9572316430521306,
        0.94268860498062101,
        0.92772535369376719,
        0.88314868768977373,
        0.81781130464382112,
        0.76554845436522456,
        0.71988664072852804,
        0.64350636142529505,
        0.59281977672104502,
        0.54547323706318263
    ]
)

libor_curve = ForwardRateCurve(
    [
        date(2019, 11, 23),
        date(2020, 11, 23),
        date(2021, 11, 23),
        date(2022, 11, 23),
        date(2023, 11, 23),
        date(2024, 11, 23),
        date(2025, 11, 23),
        date(2026, 11, 23),
        date(2027, 11, 23),
        date(2028, 11, 23),
        date(2029, 11, 23),
        date(2030, 11, 23),
        date(2031, 11, 23),
        date(2034, 11, 23),
        date(2039, 11, 23),
        date(2044, 11, 23),
        date(2049, 11, 23),
        date(2059, 11, 23),
        date(2069, 11, 23),
        date(2079, 11, 23)
    ],
    
    [
        0.01,
        0.010025,
        0.0101,
        0.010225,
        0.0104,
        0.010625,
        0.0109,
        0.011225,
        0.0116,
        0.012025,
        0.0125,
        0.013025,
        0.0136,
        0.014225,
        0.0149,
        0.015625,
        0.0164,
        0.017225,
        0.0181,
        0.019025
    ]
)
