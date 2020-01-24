__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from strategies.fixed_system import fixed_system
import random
import matplotlib.pyplot as plt

# Notes
# FIXME Odds = 1/(win_rate/100.0) -> where I put the payout?

# General Input
samples = 20
win_rate = 55 # win_rate: 0-100
payout_rate = 80 # payout_rate: 0-100 generally, but you choose
bankroll = 10000
bet_count = 1000

# Fixed System Input
bet_percentage = 2 # bet percentage 0-100


def main():
    for _ in range(samples):        
        btX, brY = fixed_system(
            generate_random_bet_result, 
            win_rate, 
            payout_rate,
            bankroll, 
            bet_count,
            bet_percentage
        )
        #plt.subplot(1, 1)
        plt.plot(btX, brY, linewidth = 0.6)
        plt.ylabel('Bankroll')
        plt.xlabel('Bet Count')
        plt.axhline(bankroll, color = 'b', linewidth = 0.1)
        plt.axhline(0, color = 'r', linewidth = 2)
    plt.show()


def generate_random_bet_result(win_rate: int) -> bool:
    result = random.randint(1,100)
    if result <= win_rate:  # (1-50 -> 50%)   ----- (1-60 -> 60%)
        return True
    elif result > win_rate: # (51-100 -> 50%) ----- (61-100 -> 40%)
        return False
    
    
if __name__ == '__main__':
    main()