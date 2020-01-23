__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import Callable, Union, Tuple


def fixed_system(
        gen_bet_result: Callable[[int], bool], 
        win_rate: int,  
        bankroll: Union[int, float], 
        bet_percentage: int, 
        wager_count: int
) -> Tuple[int, Union[int, float]]:
    
    wager_count_history_X = []
    bankroll_history_Y = []
    wager = bankroll*bet_percentage/100.0
    currentWager = 1
    
    while currentWager <= wager_count:
        if gen_bet_result(win_rate):
            bankroll += wager
        else:
            bankroll -= wager
            if bankroll <= 0:
                print('Broke')
                break
        wager_count_history_X.append(currentWager)
        bankroll_history_Y.append(bankroll)
        currentWager += 1
        
    return wager_count_history_X, bankroll_history_Y