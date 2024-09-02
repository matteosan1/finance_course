from numpy.random import seed, uniform, randint, choice

seed(1)
print ("uniform distributed floats with seed 1")
print(f"{uniform()}, {uniform()}")

seed(2)
print ("uniform distributed floats with seed 2")
print(f"{uniform()}, {uniform()}")

seed(1)
print ("uniform distributed floats with seed 1 again")
print(f"{uniform()}, {uniform()}")

print(f"random integer between 1-9: {randint(1, 10)}")

aList = ['a', 'b', 'c', 'd', 'f']
print (f"choose two items among aList: {choice(aList, size=2, replace=False)}")
