__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from strategies.fixed_system import fixed_system
import random
import matplotlib.pyplot as plt

# Notes
# FIXME Odds = 1/(win_rate/100.0) -> where I put the payout?

# General Input
samples = 100
win_rate = 0.5850 # win_rate: 0.0000-1.0000
payout_rate = 0.7800 # payout_rate: 0.0000-2.0000 generally, but you choose
bankroll = 1000
bet_count = 10000

# Fixed System Input
bet_percentage = 0.0200 # bet percentage: 0.0000-1.0000


def main():
    bust_count = 0
    for _ in range(samples):        
        btX, brY, bust = fixed_system(
            generate_random_bet_result, 
            win_rate, 
            payout_rate,
            bankroll, 
            bet_count,
            bet_percentage
        )
        
        if bust:
            bust_count += 1
        
        #plt.subplot(1, 1)
        plt.plot(btX, brY, linewidth = 0.3)
        plt.ylabel('Bankroll')
        plt.xlabel('Bet Count')
        plt.axhline(bankroll, color = 'b', linewidth = 0.1)
        plt.axhline(0, color = 'r', linewidth = 2)
    plt.show()
    print(f'{bust_count} broke of {samples} samples.')

def generate_random_bet_result(win_rate: float) -> bool:
    result = round(random.uniform(0,1),4)
    if result <= win_rate:
        return True
    elif result > win_rate: 
        return False
    
    
if __name__ == '__main__':
    main()