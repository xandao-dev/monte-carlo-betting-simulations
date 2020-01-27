from typing import Union, Tuple, List
#from .Bettor import Bettor
from .ui import print_stats
import matplotlib.pyplot as plt

"""
Strategies TODO: dAlembert, fibonacci, martingale, 
oscars_grind, patrick, sorogales, soros, whittaker
"""


class StrategiesData:
    def __init__(
            self, bet_results, general_input, specific_input):
        self.bet_results = bet_results
        self.general_input = general_input
        self.specific_input = specific_input


def fixed_bettor(
    StrategiesData
) -> Tuple[List[List[int]], List[List[Union[int, float]]]]:
    bet_results = StrategiesData.bet_results
    gi = StrategiesData.general_input
    si = StrategiesData.specific_input

    bust_count = 0
    sl_reached_count = 0
    sg_reached_count = 0
    bankroll_sum = 0
    bet_count_history_X = []
    bankroll_history_Y = []

    if gi['minimum_bet_value'] is not None:
        if si['bet_value'] < gi['minimum_bet_value']:
            print('The bet size is smaller than the minimum bet value. Bet size '
                  'will be adjusted to minimum, which is {gi["minimum_bet_value"]}.\n')
            si['bet_value'] = gi['minimum_bet_value']
    if gi['maximum_bet_value'] is not None:
        if si['bet_value'] > gi['maximum_bet_value']:
            print('The bet size is bigger than the maximum bet value. Bet size '
                  'will be adjusted to maximum, which is {gi["maximum_bet_value"]}.\n')
            si['bet_value'] = gi['maximum_bet_value']

    for sample_results in bet_results:
        bust = False
        sl_reached = False
        sg_reached = False
        bet_count_history_X_temp = [0]
        bankroll_history_Y_temp = [gi['bankroll']]
        bankroll_temp = gi['bankroll']
        for current_bet, bet_result in enumerate(sample_results, 1):
            if gi['stoploss'] is not None:
                if bankroll_temp <= gi['stoploss']:
                    sl_reached = True
                    bust = True
                    break
            if gi['stopgain'] is not None:
                if bankroll_temp >= gi['stopgain']:
                    sg_reached = True
                    break

            if bet_result:
                bankroll_temp += si['bet_value']*gi['payout_rate']
            else:
                bankroll_temp -= si['bet_value']
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
    bankroll_average = bankroll_sum/gi['samples']

    print(f'Final gi["bankroll"] average: {round(bankroll_average,2)}')
    print(f'Death rate: {round((bust_count/gi["samples"])*100,2)}%, '
          f'Survival rate: {100.0 - round((bust_count/gi["samples"])*100,2)}%')
    print(f'{bust_count} broken of {gi["samples"]} samples in Fixed Sys.!')
    print(f'{sl_reached_count} gi["stoploss"] reached of {gi["samples"]} in Fixed Sys.!')
    print(f'{sg_reached_count} gi["stopgain"] reached of {gi["samples"]} in Fixed Sys.!\n')
    return bet_count_history_X, bankroll_history_Y


def percentage_bettor(
    StrategiesData
) -> Tuple[List[List[int]], List[List[Union[int, float]]]]:
    bet_results = StrategiesData.bet_results
    gi = StrategiesData.general_input
    si = StrategiesData.specific_input

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
        bankroll_history_Y_temp = [gi['bankroll']]
        bankroll_temp = gi['bankroll']
        for current_bet, bet_result in enumerate(sample_results, 1):
            bet_value = bankroll_temp*si['bet_percentage']

            # temporary bet limiting, to minimum or maximum
            if gi['minimum_bet_value'] is not None:
                if bet_value < gi['minimum_bet_value']:
                    bet_value = gi['minimum_bet_value']
            if gi['maximum_bet_value'] is not None:
                if bet_value > gi['maximum_bet_value']:
                    bet_value = gi['maximum_bet_value']

            # bankroll_temp <= 1 because it will never bust if we dont use this.
            if bankroll_temp <= 1:
                bust = True
                break

            if gi['stoploss'] is not None:
                if bankroll_temp <= gi['stoploss']:
                    sl_reached = True
                    bust = True
                    break
            if gi['stopgain'] is not None:
                if bankroll_temp >= gi['stopgain']:
                    sg_reached = True
                    break

            if bet_result:
                bankroll_temp += bet_value*gi['payout_rate']
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
    bankroll_average = bankroll_sum/gi['samples']

    return bet_count_history_X, bankroll_history_Y


def kelly_criterion(
    StrategiesData
) -> Tuple[List[List[int]], List[List[Union[int, float]]]]:
    bet_results = StrategiesData.bet_results
    gi = StrategiesData.general_input
    si = StrategiesData.specific_input

    bust_count = 0
    sl_reached_count = 0
    sg_reached_count = 0
    bankroll_sum = 0
    bet_count_history_X = []
    bankroll_history_Y = []

    kelly_percentage = gi['win_rate'] - ((1-gi['win_rate'])/(gi['payout_rate']/1))
    if kelly_percentage <= 0:
        print('Negative Expectation. DO NOT operate!')
        return [[], []]
    for sample_results in bet_results:
        bust = False
        sl_reached = False
        sg_reached = False
        bet_count_history_X_temp = [0]
        bankroll_history_Y_temp = [gi['bankroll']]
        bankroll_temp = gi['bankroll']

        for current_bet, bet_result in enumerate(sample_results, 1):
            bet_value = bankroll_temp*kelly_percentage*si['kelly_fraction']

            # temporary bet limiting, to minimum or maximum
            if gi['minimum_bet_value'] is not None:
                if bet_value < gi['minimum_bet_value']:
                    bet_value = gi['minimum_bet_value']
            if gi['maximum_bet_value'] is not None:
                if bet_value > gi['maximum_bet_value']:
                    bet_value = gi['maximum_bet_value']

            # bankroll_temp <= 1 because it will never bust if we dont use this.
            if bankroll_temp <= 1:
                bust = True
                break

            if gi['stoploss'] is not None:
                if bankroll_temp <= gi['stoploss']:
                    sl_reached = True
                    bust = True
                    break
            if gi['stopgain'] is not None:
                if bankroll_temp >= gi['stopgain']:
                    sg_reached = True
                    break

            if bet_result:
                bankroll_temp += bet_value*gi['payout_rate']
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
    bankroll_average = bankroll_sum/gi['samples']

    print('Kelly criterion in percentage of capital: ' +
          f'{round(kelly_percentage*100,2)}%')
    return bet_count_history_X, bankroll_history_Y