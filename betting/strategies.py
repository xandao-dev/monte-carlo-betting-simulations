from typing import Union, Tuple, List
from betting.Bettor import Bettor
from betting.ui import print_stats
import matplotlib.pyplot as plt

"""
Strategies TODO: dAlembert, fibonacci, martingale, 
oscars_grind, patrick, sorogales, soros, whittaker
"""

'''
def single_bettor(wager, sample_size, number_bets, initial_funds, colour):
    num_broke = 0
    num_profitors = 0
    profits = []
    loses = []

    for i in range(sample_size):
        bettor = Bettor(initial_funds, colour)
        bettor.plot_point()
        for i in range(number_bets):
            if not bettor.broke:
                bettor.bet(wager)
            else:
                num_broke += 1
                break
        if bettor.profit > 0:
            num_profitors += 1
            profits.append(bettor.profit)
        else:
            loses.append(bettor.profit)
        plt.plot(range(len(bettor.funds_history)),
                 bettor.funds_history, colour)
    print_stats(num_broke, num_profitors, sample_size,
                profits, loses, 'Single Bettor')
'''

def fixed_bettor(
    bet_results,
    user_input,
    title = 'Fixed Bettor',
    bet_value = None
) -> Tuple[List[List[int]], List[List[Union[int, float]]]]:
    bettor = Bettor(user_input)

    sl_reached_count = 0
    sg_reached_count = 0
    broke_count = 0
    profitors_count = 0

    profits = []
    loses = []
    bet_count_histories = []
    bankroll_histories = []

    if bet_value is None:
        bet_value = user_input['bet_value']
    bet_value = bettor.max_min_verify(bet_value)

    for sample_result in bet_results:
        bankroll_history = [user_input['initial_bankroll']]
        current_bankroll = user_input['initial_bankroll']

        for bet_result in sample_result:
            current_bankroll = bettor.bet(
                bet_result, bet_value, current_bankroll)

            broke = bettor.broke_verify(current_bankroll)
            stoploss_reached = bettor.stoploss_verify(current_bankroll)
            stopgain_reached = bettor.stopgain_verify(current_bankroll)
            if broke or stoploss_reached or stopgain_reached:
                current_bankroll = bankroll_history[-1]
                break
            bankroll_history.append(current_bankroll)

        if bettor.profit(current_bankroll) > 0:
            profitors_count += 1
            profits.append(bettor.profit(current_bankroll))
        else:
            loses.append(bettor.profit(current_bankroll))
        if broke:
            broke_count += 1
        if stoploss_reached:
            sl_reached_count += 1
        if stopgain_reached:
            sg_reached_count += 1

        bankroll_histories.append(bankroll_history.copy())
    bet_count_histories = bettor.get_bet_count_histories(bankroll_histories)

    print_stats(
        user_input, bankroll_histories, broke_count, 
        profitors_count, profits, loses, title)
    return bet_count_histories, bankroll_histories, title

'''
def percentage_bettor(
    
'''

'''
def percentage_bettor(
    user_input: dict
) -> Tuple[List[List[int]], List[List[Union[int, float]]]]:
    bet_results = user_input.bet_results

    bust_count = 0
    sl_reached_count = 0
    sg_reached_count = 0
    bankroll_sum = 0
    bet_count_history_X = []
    bankroll_history_Y = []

    for sample_results in bet_results:
        bust = False
        sl_reached = False
        sg_reached = False
        bet_count_history_X_temp = [0]
        bankroll_history_Y_temp = [user_input['bankroll']]
        bankroll_temp = user_input['bankroll']
        for current_bet, bet_result in enumerate(sample_results, 1):
            bet_value = bankroll_temp*user_input['bet_percentage']

            # temporary bet limiting, to minimum or maximum
            if user_input['minimum_bet_value'] is not None:
                if bet_value < user_input['minimum_bet_value']:
                    bet_value = user_input['minimum_bet_value']
            if user_input['maximum_bet_value'] is not None:
                if bet_value > user_input['maximum_bet_value']:
                    bet_value = user_input['maximum_bet_value']

            # bankroll_temp <= 1 because it will never bust if we dont use this.
            if bankroll_temp <= 1:
                bust = True
                break

            if user_input['stoploss'] is not None:
                if bankroll_temp <= user_input['stoploss']:
                    sl_reached = True
                    bust = True
                    break
            if user_input['stopgain'] is not None:
                if bankroll_temp >= user_input['stopgain']:
                    sg_reached = True
                    break

            if bet_result:
                bankroll_temp += bet_value*user_input['payout_rate']
            else:
                bankroll_temp -= bet_value

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
    bankroll_average = bankroll_sum/user_input['samples']

    return bet_count_history_X, bankroll_history_Y


def kelly_criterion(
    user_input: dict
) -> Tuple[List[List[int]], List[List[Union[int, float]]]]:
    bet_results = user_input.bet_results

    bust_count = 0
    sl_reached_count = 0
    sg_reached_count = 0
    bankroll_sum = 0
    bet_count_history_X = []
    bankroll_history_Y = []

    kelly_percentage = user_input['win_rate'] - ((1-user_input['win_rate'])/(user_input['payout_rate']/1))
    if kelly_percentage <= 0:
        print('Negative Expectation. DO NOT operate!')
        return [[], []]
    for sample_results in bet_results:
        bust = False
        sl_reached = False
        sg_reached = False
        bet_count_history_X_temp = [0]
        bankroll_history_Y_temp = [user_input['bankroll']]
        bankroll_temp = user_input['bankroll']

        for current_bet, bet_result in enumerate(sample_results, 1):
            bet_value = bankroll_temp*kelly_percentage*user_input['kelly_fraction']

            # temporary bet limiting, to minimum or maximum
            if user_input['minimum_bet_value'] is not None:
                if bet_value < user_input['minimum_bet_value']:
                    bet_value = user_input['minimum_bet_value']
            if user_input['maximum_bet_value'] is not None:
                if bet_value > user_input['maximum_bet_value']:
                    bet_value = user_input['maximum_bet_value']

            # bankroll_temp <= 1 because it will never bust if we dont use this.
            if bankroll_temp <= 1:
                bust = True
                break

            if user_input['stoploss'] is not None:
                if bankroll_temp <= user_input['stoploss']:
                    sl_reached = True
                    bust = True
                    break
            if user_input['stopgain'] is not None:
                if bankroll_temp >= user_input['stopgain']:
                    sg_reached = True
                    break

            if bet_result:
                bankroll_temp += bet_value*user_input['payout_rate']
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
    bankroll_average = bankroll_sum/user_input['samples']

    print('Kelly criterion in percentage of capital: ' +
          f'{round(kelly_percentage*100,2)}%')
    return bet_count_history_X, bankroll_history_Y'''
