__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
# -*- coding: utf-8 -*-


from typing import Callable, Union, Tuple


def percentage_system(
        samples: int,
        gen_bet_result: Callable[[float], bool], 
        win_rate: float,
        payout_rate: float,
        bankroll: Union[int, float], 
        bet_count: int,
        bet_percentage: float,
        minimum_bet_value: int,
        stoploss: Union[int, None],
        stopgain: Union[int, None]
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
    bust_count = 0
    sl_reached_count = 0
    sg_reached_count = 0
    bet_count_history_X = []
    bankroll_history_Y = []
    for _ in range(samples):
        bust = False
        sl_reached = True
        sg_reached = False
        bet_count_history_X_temp = []
        bankroll_history_Y_temp = []
        bankroll_temp = bankroll
        for current_bet in range(1, bet_count+1):
            bet_size = bankroll_temp*bet_percentage
            
            if bet_size < minimum_bet_value:
                bust = True
                break
    
            # bankroll <= 1 because it will never bust if we dont use this.
            if bankroll_temp <= 1:
                bust = True
                break
            
            if stoploss is not None:
                if bankroll_temp <= stoploss:
                    sl_reached = True
                    break
            
            if stopgain is not None:
                if bankroll_temp >= stopgain:
                    sg_reached = True
                    break
                
            if gen_bet_result(win_rate):
                bankroll_temp += bet_size*payout_rate
            else:
                bankroll_temp -= bet_size
                
            bet_count_history_X_temp.append(current_bet)
            bankroll_history_Y_temp.append(bankroll_temp)
        
        if bust:
            bust_count += 1
        
        bet_count_history_X.append(bet_count_history_X_temp.copy())
        bankroll_history_Y.append(bankroll_history_Y_temp.copy())
    
    print(f'{bust_count} broken of {samples} samples in Percentage System!')
    return bet_count_history_X, bankroll_history_Y