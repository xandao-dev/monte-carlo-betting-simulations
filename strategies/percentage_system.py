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
) -> Tuple[List[List[int]], List[List[Union[int, float]]]]:
    '''
    Parameters
    ----------
    samples -> int
        The amount of samples that we will plot on the graph.
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
    minimum_bet_value -> int
        The minimum amount to be wagered, if the amount of the bet is less it 
        will be scaled down to the minimum amount.
    stoploss -> Union[int, None]
        If the bankroll is less than the stop loss it stops.
    stopgain -> Union[int, None]
        If the bankroll is bigger than the stop gain it stops.

    Returns
    -------
    Tuple[List[List[int]], List[List[Union[int, float]]]]
        This function returns a tuple containing two lists. The 
        first list contain the X axis lists which is the amount of bets. The 
        second list is the Y axis lists which is the bankroll history.
    '''
    bust_count = 0
    sl_reached_count = 0
    sg_reached_count = 0
    bankroll_sum = 0
    bet_count_history_X = []
    bankroll_history_Y = []
    for _ in range(samples):
        bust = False
        sl_reached = False
        sg_reached = False
        bet_count_history_X_temp = [0]
        bankroll_history_Y_temp = [bankroll]
        bankroll_temp = bankroll
        for current_bet in range(1, bet_count+1):
            bet_size = bankroll_temp*bet_percentage
            
            if bet_size < minimum_bet_value:
                bet_size = minimum_bet_value
    
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
        if sl_reached:
            sl_reached_count += 1
        if sg_reached:
            sg_reached_count += 1
            
        bet_count_history_X.append(bet_count_history_X_temp.copy())
        bankroll_history_Y.append(bankroll_history_Y_temp.copy())
        
        bankroll_sum += bankroll_history_Y_temp[-1]
    bankroll_average = bankroll_sum/samples
    print(f'{bust_count} broken of {samples} samples in Perc. Sys.!')
    print(f'Death rate: {round((bust_count/samples)*100,2)}%,', end = '')
    print(f' Survival rate: {100.0 - round((bust_count/samples)*100,2)}%')
    print(f'{sl_reached_count} stoploss reached of {samples} in Perc. Sys.!')
    print(f'{sg_reached_count} stopgain reached of {samples} in Perc. Sys.!')
    print(f'Final bankroll average: {round(bankroll_average,2)}\n')
    return bet_count_history_X, bankroll_history_Y