__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
# -*- coding: utf-8 -*-


from typing import Union, Tuple, List


def fixed_system(
        results: List[List[bool]],
        payout_rate: float,
        bankroll: Union[int, float],
        bet_value: Union[int,float],
        minimum_bet_value: Union[int, float, None],
        maximum_bet_value: Union[int, float, None],
        stoploss: Union[int, None],
        stopgain: Union[int, None]
) -> Tuple[List[List[int]], List[List[Union[int, float]]]]:
    '''
    Parameters
    ----------
    results -> List[List[bool]]
        The results are a list of betting results, the innermost lists
        represent the amount of bets and the outermost lists represent
        the number of samples.
    payout_rate -> float
        The payout rate means how much you will win, for example a 0.80 payout
        rate means that for every $ 1 wagered you will win $1 * 0.80 = 0.80c.
        Here the payout rate varies from less infinite to more infinite, but
        this value generally ranges from 0.0000 to 2.0000.
    bankroll -> Union[int, float]
        The bankroll is the amount of money you have to bet.
    bet_value -> Union[int,float]
        The size of the bet, which in this system is fixed.
    minimum_bet_value -> Union[int, float, None]
        The minimum bet value is to avoid making miserably small bets. If the
        amount of the bet is less than minimum bet value it will be scaled 
        down to the minimum amount. Put None to disable.
    maximum_bet_value -> Union[int, float, None]
        The maximum bet value is to avoid making non real big bets. If the
        amount of the bet is bigger than the maximum bet value, it will be 
        scaled to maximum amount. Put None to disable.
    stoploss -> Union[int, None]
        If the bankroll is less than the stop loss it stops.
        Put None to disable.
    stopgain -> Union[int, None]
        If the bankroll is bigger than the stop gain it stops.
        Put None to disable.

    Returns
    -------
    Tuple[List[List[int]], List[List[Union[int, float]]]]
        This function returns a tuple containing two lists. The
        first list contain the X axis lists which is the amount of bets. The
        second list is the Y axis lists which is the bankroll history.
    '''
    
    print('*FIXED SYSTEM*')
    
    bust_count = 0
    sl_reached_count = 0
    sg_reached_count = 0
    bankroll_sum = 0
    bet_count_history_X = []
    bankroll_history_Y = []

    samples = len(results) #It's equal to the number of samples of main.py
    if minimum_bet_value is not None:
        if bet_value < minimum_bet_value:
            print('The bet size is smaller than the minimum bet value. Bet size '
                  'will be adjusted to minimum, which is {minimum_bet_value}.\n')
            bet_value = minimum_bet_value
    if maximum_bet_value is not None:
        if bet_value > maximum_bet_value:
            print('The bet size is bigger than the maximum bet value. Bet size '
                  'will be adjusted to maximum, which is {maximum_bet_value}.\n')
            bet_value = maximum_bet_value
        
    for sample_results in results:
        bust = False
        sl_reached = False
        sg_reached = False
        bet_count_history_X_temp = [0]
        bankroll_history_Y_temp = [bankroll]
        bankroll_temp = bankroll
        for current_bet, bet_result in enumerate(sample_results,1):
            if stoploss is not None:
                if bankroll_temp <= stoploss:
                    sl_reached = True
                    break
            if stopgain is not None:
                if bankroll_temp >= stopgain:
                    sg_reached = True
                    break

            if bet_result:
                bankroll_temp += bet_value*payout_rate
            else:
                bankroll_temp -= bet_value
                if bankroll_temp <= 0:
                    bust = True
                    break

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

    print(f'Final bankroll average: {round(bankroll_average,2)}')
    print(f'Death rate: {round((bust_count/samples)*100,2)}%, '
          f'Survival rate: {100.0 - round((bust_count/samples)*100,2)}%')
    print(f'{bust_count} broken of {samples} samples in Fixed Sys.!')
    print(f'{sl_reached_count} stoploss reached of {samples} in Fixed Sys.!')
    print(f'{sg_reached_count} stopgain reached of {samples} in Fixed Sys.!\n')
    return bet_count_history_X, bankroll_history_Y