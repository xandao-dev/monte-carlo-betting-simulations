__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from strategies.fixed_system import fixed_system
from strategies.percentage_system import percentage_system
from strategies.kelly_criterion import kelly_criterion
from typing import Union, List
import random
import matplotlib.pyplot as plt
import matplotlib.style as style


style.use('bmh')


# General Input
samples = 1
win_rate = 0.5500 # win rate: 0.0000-1.0000
payout_rate = 0.8500 # payout rate: 0.0000-2.0000 generally, but you choose
bankroll = 500
bet_count = 10000
stoploss = None
stopgain = None

# Fixed System and Percentage System Input
bet_percentage = 0.0200 # bet percentage: 0.0000-1.0000

# Percentage System and Kelly Criterion Input
#FIXME add to kelly criterion
minimum_bet_value = 2

# Kelly Criterion Input
kelly_fraction = 1 # kelly fraction: 0.0000-1.0000, generally 1, 0.5 or 0.25


if bankroll*bet_percentage <= minimum_bet_value:
    bet_percentage = minimum_bet_value/100.0  
    print(f'Bet size is less than minimum bet value! Adjusting the bet ' +
          f'percentage to {bet_percentage}\n')
    
    
def main():   
    betX, bkrY = fixed_system(
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
    plot_config('Fixed System', betX, bkrY, False)

    betX, bkrY = percentage_system(
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
    plot_config('Percentage System', betX, bkrY, False)

    betX, bkrY = kelly_criterion(
        samples,
        generate_random_bet_result, 
        win_rate, 
        payout_rate,
        bankroll, 
        bet_count,
        kelly_fraction,
        minimum_bet_value,
        stoploss,
        stopgain
    )
    plot_config('Percentage System', betX, bkrY, False)
    
    plt.show()


def generate_random_bet_result(win_rate: float) -> bool:
    result = round(random.uniform(0,1),4)
    if result <= win_rate:
        return True
    elif result > win_rate: 
        return False
    
    
def plot_config(
        title: str, 
        bet_count_history_X: List[List[int]], 
        bankroll_history_Y: List[List[Union[int, float]]],
        new_fig = True
) -> None:
    if new_fig:
        plt.figure()
    for x, y in zip(bet_count_history_X, bankroll_history_Y):
        plt.plot(x, y, linewidth = 0.6)   
    plt.title(title)
    plt.ylabel('Bankroll')
    plt.xlabel('Bet Count')
    plt.axhline(bankroll, color = 'b', linewidth = 0.5)
    plt.axhline(0, color = 'r', linewidth = 2)


if __name__ == '__main__':
    main()