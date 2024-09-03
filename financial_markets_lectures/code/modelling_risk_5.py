from random import seed, random

seed(1)
Pdef = 0.2
trials = 10000
defaults = 0
for _ in range(trials):
    credit_event = random()
    if credit_event <= Pdef:
        defaults += 1

print (defaults/trials)