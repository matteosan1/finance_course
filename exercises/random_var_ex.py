ex_roll = 0
for i in range(2, 7):
    ex_roll += 1/6*i
print (ex_roll)


from matplotlib import pyplot as plt
exps = []
for k in range(1, 51):
    exp = -k*1/6
    for i in range(2, 7):
        exp += 1/6*i
    exps.append(exp)
fig = plt.figure(figsize=(10,8))
plt.plot(range(1, 51), exps)
plt.grid(True)
plt.xlabel("current turn points (k)")
plt.ylabel("expected points next roll")
plt.show()






def F(x):
    return x**3/27000
P = F(20)-F(15)
print (P)

def tot(x):
    return x**4/36000
print (tot(30))

expected = 1 * (F(20)-F(10)) + 1.5 * (F(25)-F(20)) + 3 * (F(30)-F(25))
print (expected)

xmin = 10*0.96
xmax = 15*0.96
P = F(xmax)-F(xmin)
print (P)







P = {7:0.10, 8:0.20, 10:0.30, 11:0.10}
P[9] = 1-(P[7]+P[8]+P[10]+P[11])
print (P[9])

expected_days = sum([d*p for d, p in P.items()])
var_days = sum([p*(d**2) for d, p in P.items()]) - expected_days**2
E_C = 12000+300*expected_days
print (E_C)


b = 300
print (b**2 * var_days)










from scipy.stats import norm
# convert the two limits in the standard normal
xmin = (150-600)/360
xmax = (1050-600)/360
print (xmin, xmax)
print (norm.cdf(xmax)-norm.cdf(xmin))


xmin = (150-600)/420
xmax = (1050-600)/420
print (xmin, xmax)
print (norm.cdf(xmax)-norm.cdf(xmin))


xmin = 504/360
print (xmin)
# the factor 2 because the win can exceed both ways the mean
print (norm.cdf(-xmin) * 2)




