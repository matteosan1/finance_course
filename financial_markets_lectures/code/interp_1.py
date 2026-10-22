from scipy.interpolate import interp1d

t = [1, 2, 4]
dfs = [0.994, 0.982, 0.965]

inter = interp1d(t, dfs)	
print (f"{inter(1.5):.3f}")