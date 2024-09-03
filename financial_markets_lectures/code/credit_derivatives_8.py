N=10
# probabilities of default of the each name
q = [0.01, 0.02, 0.15, 0.22, 0.03, 0.01, 0.024, 0.008, 0.015, 0.04]

# p[k] probability of k defaults
p = [0 for _ in range(0, N+1)]
p[0] = (1-q[0])
p[1] = q[0]
for i in range(2, N+1):
    for j in range(1, i+1):
        p[j] = p[j-1]*q[i-1] + p[j]*(1-q[i-1])
    p[0] = p[0]*(1-q[i-1])
print (p)
