import math

ith = []
maturity = [0.5, 1, 1.5, 2]
coupon = [0, 0, 6, 10]
price = [96, 92.10, 98.5, 105.9]

def zcb(P, N, tau):
    v = N/P
    return math.pow(v, 1/tau) - 1

def i(P, c, tau, ith):
    den = P
    for i in range(int(tau*2)):
        den -= c/2*math.pow(1 + ith[i], -i)
    return math.pow((1+c/2)/den, 1/k/tau) - 1 

# 0.085069
# 0.068392
ith.append(zcb(price[0], 100, maturity[0]))
ith.append(zcb(price[1], 100, maturity[1]))
print (i(price[2], 6, 1.5, ith))
       
