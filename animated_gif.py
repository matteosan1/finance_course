# define the domain of inputs
import numpy as np
from numpy.random import choice, seed
from scipy.stats import norm
import matplotlib.pyplot as plt

#def deck_sim(experiments):
#    successes = 0
#    for i in range(experiments):
#       cards = choice(deck, 2, replace=False)
##        #if i < 10:
##        #  print (cards)
#       if all(cards == 10):
#           successes += 1
#    return successes
#
#deck = [1,2,3,4,5,6,7,8,9,10] * 4
#
#experiments = 500
#trials = 10000
#r = []
#for e in range(experiments):
##    if (e%100 == 0):
##        print (e)
#    seed(e)
#    successes = deck_sim(trials)
##    #print (successes/trials)
#    r.append(successes/trials)
#
#with open("data_avg.npy", "wb") as f:
#    np.save(f, np.array(r))
    
from scipy.stats import norm

with open("data.npy", "rb") as f:
    r = np.load(f)

params = []
for i in [30, 500, 1000, 5000]:
    sample = np.random.choice(r, i)
    params.append((np.mean(sample), np.std(sample)/np.sqrt(i)))

tv = 1/130
x = np.arange(0.0072, 0.0082, 0.000001) 
for p in params:
    plt.plot(x, norm(*p).pdf(x))
plt.vlines(tv, 0, 30000, color='black')
plt.xlim(0.0074, 0.008)
plt.ylim(0, 35000)
plt.show()

#plt.hist(avg, range=(.0074, .0078), bins=20, histtype="stepfilled", edgecolor='blue', color='lightblue')
#plt.savefig(f"pics/plt_mean.png")


#for i in range(len(r)):
#    plt.hist(r[:i], range=(0.005, .015), bins=99,  edgecolor='blue', color='lightblue')
#    plt.xlim(0.005, 0.0105)
#    plt.ylim(0, 250)
#    plt.savefig(f"pics/plt_{i}.png")
#    plt.clf()
#
#i += 1
#x = np.linspace(0.005, 0.015, 99)
#N = norm.pdf(x, np.mean(r), np.std(r))
#
#plt.hist(r, range=(0.005, .015), bins=99,  edgecolor='blue', color='lightblue')
#plt.plot(x, 1/(np.std(r)*np.sqrt(2*np.pi))*0.0011*N, color='red')
#plt.xlim(0.005, 0.0105)
#plt.ylim(0, 250)
##plt.show()
#plt.savefig(f"pics/plt_{i}.png")


#from PIL import Image
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#import copy
#
#def update(i):
#    im.set_array(image_arrays[i])
#    return im
#
#image_array = []
#for i in range(0, 5001):
#    image = copy.deepcopy(Image.open(f"pics/plt_{i}.png"))
#    image_array.append(image)
#
#fig, ax = plt.subplots()
#im = ax.imshow(image_arrays[0], animated=True)
#
#animation_fig = animation.FuncAnumation(fig, update, frames=len(image_arrays),
#                                        interval=200, blit=True, repeat_delay=10)
#plt.show()
#animation_fig.show("animated_experiment.gif")
    
