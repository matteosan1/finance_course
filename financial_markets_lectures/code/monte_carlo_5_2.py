import time

seed(1)
trials = [100, 1000, 10000, 100000, 1000000]
for i, t in enumerate(trials):
    t1 = time.time()
    in_circle = simulation(t)
    t2 = time.time() - t1
    print (f"pi={in_circle/t*4:.6f} {t2:.4f}s")