__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import Callable, Union, Tuple


def fixed_system(
        gen_bet_result: Callable[[float], bool], 
        win_rate: float,
        payout_rate: float,
        bankroll: Union[int, float], 
        bet_count: int,
        bet_percentage: float
) -> Tuple[int, Union[int, float]]:
    '''
    Parameters
    ----------
    gen_bet_result -> Callable[[float], bool]
        A function that generate a random bet result, considering the win rate,
        and return True for win or False for lose.
    win_rate -> float
        The win rate is a rate that can range from 0.0000 to 1.0000, which 
        means the percentage you have of winning. 
        To know your win rate you must divide the total bets you won by the 
        total bet, the more bets the more 
        accurate that rate will be.
    payout_rate -> float
        The payout rate means how much you will win, for example a 0.80 payout
        rate means that for every $ 1 wagered you will win $1 * 0.80 = 0.80c. 
        Here the payout rate varies from less infinite to more infinite, but 
        this value generally ranges from 0.0000 to 2.0000.
    bankroll -> Union[int, float]
        The bankroll is the amount of money you have to bet.
    bet_count -> int
        The bet count is the amount of bets you will simulate.
    bet_percentage -> float
        The bet percentage is the amount you will risk on each bet. This value
        can range from 0.0000 to 1.0000.

    Returns
    -------
    Tuple[int, Union[int, float]]
        This function returns a tuple containing two lists and a int. The 
        first is the X axis which is the amount of bets. The second is the 
        Y axis which is the bankroll history. The third is whether it is bust 
        or not.
    '''
 
    bust = False
    bet_count_history_X = []
    bankroll_history_Y = []
    bet_size = bankroll*bet_percentage
    for current_bet in range(1, bet_count+1):
        if gen_bet_result(win_rate):
            bankroll += bet_size*payout_rate
        else:
            bankroll -= bet_size
            if bankroll <= 0:
                bust = True
                break
        bet_count_history_X.append(current_bet)
        bankroll_history_Y.append(bankroll)
    return bet_count_history_X, bankroll_history_Y, bust