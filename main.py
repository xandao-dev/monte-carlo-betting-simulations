__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from strategies.fixed_system import fixed_system
import random
import matplotlib.pyplot as plt


def generate_random_bet_result(win_rate: int) -> bool:
    result = random.randint(1,100)
    if result <= win_rate:  # (1-50 -> 50%)   ----- (1-60 -> 60%)
        return True
    elif result > win_rate: # (51-100 -> 50%) ----- (61-100 -> 40%)
        return False
    

x=0
while x < 100:             
    wX, bY = fixed_system(generate_random_bet_result, 49, 10000, 10, 1000)
    #plt.subplot(1, 1)
    plt.plot(wX, bY)
    plt.ylabel('Bankroll')
    plt.xlabel('Wager Count')
    plt.axhline(10000, color = 'b')
    plt.axhline(0, color = 'r')
    x+=1

plt.show()
