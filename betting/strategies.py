from typing import Union, Tuple, List
from betting.Bettor import Bettor
from betting.ui import print_strategy_stats
import matplotlib.pyplot as plt

"""
Strategies TODO: dAlembert, fibonacci,
oscars_grind, patrick, sorogales, soros, whittaker
"""
strategies = ['fixed_bettor', 'percentage_bettor', 'kelly_criterion', 
              'fixed_martingale', 'percentage_martingale']


def fixed_bettor(
    bet_results,
    user_input,
    title='Fixed Bettor',
    bet_value=None
) -> Tuple[List[List[int]], List[List[Union[int, float]]], str]:
    bettor = Bettor(user_input)

    sl_reached_count = 0
    sg_reached_count = 0
    broke_count = 0
    profitors_count = 0

    profits = []
    loses = []
    bet_count_histories = []
    bankroll_histories = []

    if bet_value is not None:
        user_input['bet_value'] = bet_value 
    user_input['bet_value'] = bettor.max_min_verify(user_input['bet_value'])

    for sample_result in bet_results:
        bankroll_history = [user_input['initial_bankroll']]
        current_bankroll = user_input['initial_bankroll']

        for bet_result in sample_result:
            current_bankroll = bettor.bet(
                bet_result, user_input['bet_value'], current_bankroll)

            broke = bettor.broke_verify(current_bankroll)
            stoploss_reached = bettor.stoploss_verify(current_bankroll)
            stopgain_reached = bettor.stopgain_verify(current_bankroll)
            if broke or stoploss_reached or stopgain_reached:
                current_bankroll = bankroll_history[-1]
                break
            bankroll_history.append(current_bankroll)

        if bettor.profit(current_bankroll) > 0 and not (broke or stoploss_reached):
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

    print_strategy_stats(
        user_input, bankroll_histories, broke_count,
        profitors_count, profits, loses, title)
    return bet_count_histories, bankroll_histories, title


def percentage_bettor(
    bet_results,
    user_input,
    title='Percentage Bettor',
    bet_percentage=None
) -> Tuple[List[List[int]], List[List[Union[int, float]]], str]:
    bettor = Bettor(user_input)

    sl_reached_count = 0
    sg_reached_count = 0
    broke_count = 0
    profitors_count = 0

    profits = []
    loses = []
    bet_count_histories = []
    bankroll_histories = []

    if bet_percentage is None:
        bet_percentage = user_input['bet_percentage']

    for sample_result in bet_results:
        bankroll_history = [user_input['initial_bankroll']]
        current_bankroll = user_input['initial_bankroll']

        for bet_result in sample_result:
            bet_value = current_bankroll*bet_percentage
            bet_value = bettor.max_min_verify(bet_value)

            current_bankroll = bettor.bet(
                bet_result, bet_value, current_bankroll)

            broke = bettor.broke_verify(current_bankroll, broke_value=1)
            stoploss_reached = bettor.stoploss_verify(current_bankroll)
            stopgain_reached = bettor.stopgain_verify(current_bankroll)
            if broke or stoploss_reached or stopgain_reached:
                current_bankroll = bankroll_history[-1]
                break
            bankroll_history.append(current_bankroll)

        if bettor.profit(current_bankroll) > 0 and not (broke or stoploss_reached):
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

    print_strategy_stats(
        user_input, bankroll_histories, broke_count,
        profitors_count, profits, loses, title)
    return bet_count_histories, bankroll_histories, title


def kelly_criterion(
    bet_results,
    user_input,
    title='Kelly Criterion',
    kelly_fraction=1
) -> Tuple[List[List[int]], List[List[Union[int, float]]], str]:
    bettor = Bettor(user_input)

    sl_reached_count = 0
    sg_reached_count = 0
    broke_count = 0
    profitors_count = 0

    profits = []
    loses = []
    bet_count_histories = []
    bankroll_histories = []

    kelly_percentage = user_input['win_rate'] - \
        ((1-user_input['win_rate'])/(user_input['payout_rate']/1))
    if kelly_percentage <= 0:
        print(f'\n*{title.upper()}*')
        print('Negative Expectation. DO NOT operate!')
        # FIXME the script are ploting an empty graph
        return [[], [], title]

    for sample_result in bet_results:
        bankroll_history = [user_input['initial_bankroll']]
        current_bankroll = user_input['initial_bankroll']

        for bet_result in sample_result:
            bet_value = current_bankroll*kelly_percentage*kelly_fraction
            bet_value = bettor.max_min_verify(bet_value)

            current_bankroll = bettor.bet(
                bet_result, bet_value, current_bankroll)

            broke = bettor.broke_verify(current_bankroll, broke_value=1)
            stoploss_reached = bettor.stoploss_verify(current_bankroll)
            stopgain_reached = bettor.stopgain_verify(current_bankroll)
            if broke or stoploss_reached or stopgain_reached:
                current_bankroll = bankroll_history[-1]
                break
            bankroll_history.append(current_bankroll)

        if bettor.profit(current_bankroll) > 0 and not (broke or stoploss_reached):
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

    print_strategy_stats(
        user_input, bankroll_histories, broke_count,
        profitors_count, profits, loses, title, kelly_percentage)
    return bet_count_histories, bankroll_histories, title


def fixed_martingale(
    bet_results,
    user_input,
    title='Fixed Martingale',
    bet_value=None,
    multiplication_factor=2,
    round_limit=10,
    inverted=False
) -> Tuple[List[List[int]], List[List[Union[int, float]]], str]:
    bettor = Bettor(user_input)

    current_round = 0
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
    initial_bet_value = bet_value

    for sample_result in bet_results:
        bankroll_history = [user_input['initial_bankroll']]
        current_bankroll = user_input['initial_bankroll']

        for i, bet_result in enumerate(sample_result):
            if not inverted:
                if sample_result[i-1] == False and i > 0 and current_round < round_limit:
                    bet_value = multiplication_factor*bet_value
                    bet_value = bettor.max_min_verify(bet_value)
                    current_round += 1
                else:
                    bet_value = initial_bet_value
                    current_round = 0
            else:
                if sample_result[i-1] == True and i > 0 and current_round < round_limit:
                    bet_value = multiplication_factor*bet_value
                    bet_value = bettor.max_min_verify(bet_value)
                    current_round += 1
                else:
                    bet_value = initial_bet_value
                    current_round = 0

            current_bankroll = bettor.bet(
                bet_result, bet_value, current_bankroll)

            broke = bettor.broke_verify(current_bankroll)
            stoploss_reached = bettor.stoploss_verify(current_bankroll)
            stopgain_reached = bettor.stopgain_verify(current_bankroll)
            if broke or stoploss_reached or stopgain_reached:
                current_bankroll = bankroll_history[-1]
                break
            bankroll_history.append(current_bankroll)

        if bettor.profit(current_bankroll) > 0 and not (broke or stoploss_reached):
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

    print_strategy_stats(
        user_input, bankroll_histories, broke_count,
        profitors_count, profits, loses, title)
    return bet_count_histories, bankroll_histories, title


def percentage_martingale(
    bet_results,
    user_input,
    title='Percentage Martingale',
    bet_percentage=None,
    use_kelly_percentage=False,
    multiplication_factor=2,
    round_limit=10,
    inverted=False
) -> Tuple[List[List[int]], List[List[Union[int, float]]], str]:
    bettor = Bettor(user_input)

    current_round = 0
    sl_reached_count = 0
    sg_reached_count = 0
    broke_count = 0
    profitors_count = 0

    profits = []
    loses = []
    bet_count_histories = []
    bankroll_histories = []

    if bet_percentage is None:
        bet_percentage = user_input['bet_percentage']
    if use_kelly_percentage:
        bet_percentage = user_input['win_rate'] - \
            ((1-user_input['win_rate'])/(user_input['payout_rate']/1))
        if bet_percentage <= 0:
            print(f'\n*{title.upper()}*')
            print('Negative Expectation. DO NOT operate!')
            # FIXME the script are ploting an empty graph
            return [[], [], title]

    for sample_result in bet_results:
        bankroll_history = [user_input['initial_bankroll']]
        current_bankroll = user_input['initial_bankroll']

        for i, bet_result in enumerate(sample_result):
            initial_bet_value = current_bankroll*bet_percentage
            initial_bet_value = bettor.max_min_verify(initial_bet_value)
            if not inverted:
                if sample_result[i-1] == False and i > 0 and current_round < round_limit:
                    bet_value = multiplication_factor*bet_value
                    bet_value = bettor.max_min_verify(bet_value)
                    current_round += 1
                else:
                    bet_value = initial_bet_value
                    current_round = 0
            else:
                if sample_result[i-1] == True and i > 0 and current_round < round_limit:
                    bet_value = multiplication_factor*bet_value
                    bet_value = bettor.max_min_verify(bet_value)
                    current_round += 1
                else:
                    bet_value = initial_bet_value
                    current_round = 0

            current_bankroll = bettor.bet(
                bet_result, bet_value, current_bankroll)

            broke = bettor.broke_verify(current_bankroll)
            stoploss_reached = bettor.stoploss_verify(current_bankroll)
            stopgain_reached = bettor.stopgain_verify(current_bankroll)
            if broke or stoploss_reached or stopgain_reached:
                current_bankroll = bankroll_history[-1]
                break
            bankroll_history.append(current_bankroll)

        if bettor.profit(current_bankroll) > 0 and not (broke or stoploss_reached):
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

    if not use_kelly_percentage:
        print_strategy_stats(
            user_input, bankroll_histories, broke_count,
            profitors_count, profits, loses, title)
    else:
        print_strategy_stats(
            user_input, bankroll_histories, broke_count,
            profitors_count, profits, loses, title,
            kelly_percentage=bet_percentage)
    return bet_count_histories, bankroll_histories, title
