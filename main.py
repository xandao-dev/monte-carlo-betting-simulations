__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Notes
# FIXME Odds = 1/(win_rate/100.0) -> where I put the payout?


from strategies.fixed_system import fixed_system
from strategies.percentage_system import percentage_system
import random
import matplotlib.pyplot as plt
import matplotlib.style as style


style.use('bmh')


# General Input
samples = 2
win_rate = 0.5500 # win_rate: 0.0000-1.0000
payout_rate = 0.8800 # payout_rate: 0.0000-2.0000 generally, but you choose
bankroll = 100
bet_count = 10000


# Fixed System and Percentage System Input
bet_percentage = 0.0100 # bet percentage: 0.0000-1.0000
stoploss = None
stopgain = None


# Percentage System Input
minimum_bet_value = 2


if bankroll*bet_percentage <= minimum_bet_value:
    bet_percentage = minimum_bet_value/100.0  
    print(f'Bet size is less than minimum bet value! Adjusting the bet ' +
          f'percentage to {bet_percentage}\n')
    
    
def main():   
    btX, brY = fixed_system(
        samples,
        generate_random_bet_result, 
        win_rate, 
        payout_rate,
        bankroll, 
        bet_count,
        bet_percentage,
        stoploss,
        stopgain
    )
    
    plt.figure()
    for x, y in zip(btX, brY):
        plt.plot(x, y, linewidth = 0.6) 
    plt.title('Fixed System')
    plt.ylabel('Bankroll')
    plt.xlabel('Bet Count')
    plt.axhline(bankroll, color = 'b', linewidth = 0.5)
    plt.axhline(0, color = 'r', linewidth = 2)

    btX, brY = percentage_system(
        samples,
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
    
    plt.figure()
    for x, y in zip(btX, brY):
        plt.plot(x, y, linewidth = 0.6)   
    plt.title('Percentage System')
    plt.ylabel('Bankroll')
    plt.xlabel('Bet Count')
    plt.axhline(bankroll, color = 'b', linewidth = 0.5)
    plt.axhline(0, color = 'r', linewidth = 2)
    
    plt.show()


def generate_random_bet_result(win_rate: float) -> bool:
    result = round(random.uniform(0,1),4)
    if result <= win_rate:
        return True
    elif result > win_rate: 
        return False
    
    
if __name__ == '__main__':
    main()