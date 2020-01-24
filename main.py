__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from strategies.fixed_system import fixed_system
from strategies.percentage_system import percentage_system
import random
import matplotlib.pyplot as plt

# Notes
# FIXME Odds = 1/(win_rate/100.0) -> where I put the payout?

# General Input
samples = 500
win_rate = 0.5000 # win_rate: 0.0000-1.0000
payout_rate = 1.0000 # payout_rate: 0.0000-2.0000 generally, but you choose
bankroll = 100
bet_count = 10000

# Fixed System and Percentage System Input
bet_percentage = 0.0100 # bet percentage: 0.0000-1.0000
minimum_bet_value = 2
stoploss = None
stopgain = None


if bankroll*bet_percentage <= minimum_bet_value:
    bet_percentage = minimum_bet_value/100.0  
    print(f'Bet size is less than minimum bet value! Adjusting the bet ' +
          f'percentage to {bet_percentage}')
    
    
def main():  

    bust_count1 = 0
    bust_count2 = 0 
    fig, axs = plt.subplots(2)
    for _ in range(samples):        
        btX, brY, bust1 = fixed_system(
            generate_random_bet_result, 
            win_rate, 
            payout_rate,
            bankroll, 
            bet_count,
            bet_percentage,
            minimum_bet_value,
            stoploss,
            stopgain
        )
        axs[0].plot(btX, brY, linewidth = 0.3)
        if bust1:
            bust_count1 += 1
            
        btX, brY, bankroll2, bust2,stop_gain_reached = percentage_system(
            generate_random_bet_result, 
            win_rate, 
            payout_rate,
            bankroll, 
            bet_count,
            bet_percentage,
            minimum_bet_value,
            stoploss,
            stopgain
        )

        axs[1].plot(btX, brY, linewidth = 0.8)
        if bust2:
            bust_count2 += 1

    axs[0].set_title('Fixed System')
    axs[1].set_title('Percentage System')
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    for ax in axs:
        ax.set_ylabel('Bankroll')
        ax.set_xlabel('Bet Count')
        ax.axhline(bankroll, color = 'b', linewidth = 0.5)
        ax.axhline(0, color = 'r', linewidth = 2)
    plt.show()
    print(f'{bust_count1} broke of {samples} samples.')
    print(f'{bust_count2} broke of {samples} samples.')

def generate_random_bet_result(win_rate: float) -> bool:
    result = round(random.uniform(0,1),4)
    if result <= win_rate:
        return True
    elif result > win_rate: 
        return False
    
    
if __name__ == '__main__':
    main()