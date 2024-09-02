from numpy.random import choice, seed

def draw_sim(trials=10000, debug=False):
    deck = ["A", "2", "3", "4", "5", "6", "7", "J", "Q", "K"] * 4
    successes = 0

    for i in range(trials):
        cards = choice(deck, k=2, replace=False)
        if debug and i < 10:
            print (cards)
        if all(cards == "K"):
            successes += 1
    return successes/trials
            
seed(1)
trials = 1000000        
print (f"The probability to draw two kings is {draw_sim(trials, True):.4f}")