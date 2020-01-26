__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
# -*- coding: utf-8 -*-


from typing import Union, Tuple, List


def kelly_criterion(
        results: List[List[bool]],
        win_rate: float,
        payout_rate: float,
        bankroll: Union[int, float],
        kelly_fraction: float,
        minimum_bet_value: Union[int, float],
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
    win_rate : float
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
    kelly_fraction -> float
        The fraction of kelly is a fraction of the percentage generated,
        changing it can cause overbet or underbet. It can range from 0.0000
        to +infinite, but generally 1, 0.5 or 0.25.
    minimum_bet_value -> Union[int, float]
        The minimum amount to be wagered, if the amount of the bet is less it
        will be scaled down to the minimum amount until it can be changed.
        Put None to disable.
    maximum_bet_value -> Union[int, float, None]
        The maximum bet value is to avoid making non real big bets. If the
        amount of the bet is bigger than the maximum bet value, it will be 
        scaled to maximum amount until it can be changed. Put None to disable.
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
    
    print('*KELLY CRITERION*')
    
    bust_count = 0
    sl_reached_count = 0
    sg_reached_count = 0
    bankroll_sum = 0
    bet_count_history_X = []
    bankroll_history_Y = []

    samples = len(results) #It's equal to the number of samples of main.py
    kelly_percentage = win_rate - ((1-win_rate)/(payout_rate/1))
    if kelly_percentage <= 0:
        print('Negative Expectation. DO NOT operate!')
        return [[],[]]
    for sample_results in results:
        bust = False
        sl_reached = False
        sg_reached = False
        bet_count_history_X_temp = [0]
        bankroll_history_Y_temp = [bankroll]
        bankroll_temp = bankroll

        for current_bet, bet_result in enumerate(sample_results,1):
            bet_value = bankroll_temp*kelly_percentage*kelly_fraction
            
            #temporary bet limiting, to minimum or maximum
            if minimum_bet_value is not None: 
                if bet_value < minimum_bet_value:
                    bet_value = minimum_bet_value
            if maximum_bet_value is not None:
                if bet_value > maximum_bet_value:
                    bet_value = maximum_bet_value
            
            # bankroll_temp <= 1 because it will never bust if we dont use this.
            if bankroll_temp <= 1 :
                bust = True
                break
            
            if stoploss is not None:
                if bankroll_temp <= stoploss:
                    sl_reached = True
                    bust = True
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

    print('Kelly criterion in percentage of capital: '+
          f'{round(kelly_percentage*100,2)}%')
    print(f'Final bankroll average: {round(bankroll_average,2)}')
    print(f'Death rate: {round((bust_count/samples)*100,2)}%, '
          f'Survival rate: {100.0 - round((bust_count/samples)*100,2)}%')
    print(f'{bust_count} broken of {samples} samples in Fixed Sys.!')
    print(f'{sl_reached_count} stoploss reached of {samples} in Fixed Sys.!')
    print(f'{sg_reached_count} stopgain reached of {samples} in Fixed Sys.!\n')
    return bet_count_history_X, bankroll_history_Y