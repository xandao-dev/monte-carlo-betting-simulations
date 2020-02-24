from typing import Union, Tuple, List
from abc import ABC, abstractmethod
from random import uniform

from betting.PlotGraph import PlotGraph
from betting.Stats import Stats
from betting.statistical_calculations import *

"""
Strategies TODO: dAlembert, fibonacci,
oscars_grind, patrick, sorogales, soros, whittaker
"""
strategies_list = ['fixed_bettor', 'percentage_bettor', 'kelly_criterion',
                   'fixed_martingale', 'percentage_martingale']


class Strategies(ABC):
    def __init__(self, bet_results: List[List[bool]], user_input: dict, title: str):
        self.bet_results = bet_results
        self.user_input: dict = user_input
        self.title: str = title
        self.__bet_value = None

    def simulate_strategy(self):
        graph: PlotGraph = PlotGraph(self.user_input)

        current_bankroll: Union[int, float] = self.user_input['initial_bankroll']
        sl_reached_count: int = 0
        sg_reached_count: int = 0
        broke_count: int = 0
        profitors_count: int = 0
        profits: List[Union[int, float]] = []
        loses: List[Union[int, float]] = []
        bet_count_histories: List[List[int]] = []
        bankroll_histories: List[List[Union[int, float]]] = []
        bet_value_histories: List[List[Union[int, float]]] = []
        broke: bool = False
        stoploss_reached: bool = False
        stopgain_reached: bool = False

        self.strategy_setup()
        self.bet_value_calculator_fixed()

        for sample_result in self.bet_results:
            bankroll_history = [self.user_input['initial_bankroll']]
            bet_value_history = []
            current_bankroll = self.user_input['initial_bankroll']
            for bet_result in sample_result:
                self.bet_value_calculator_non_fixed()
                current_bankroll = self.__bet(bet_result, current_bankroll)

                broke = self.__broke_verify(current_bankroll, broke)
                stoploss_reached = self.__stoploss_verify(
                    current_bankroll, stoploss_reached)
                stopgain_reached = self.__stopgain_verify(
                    current_bankroll, stopgain_reached)
                if broke or stoploss_reached or stopgain_reached:
                    current_bankroll = bankroll_history[-1]
                    break

                bankroll_history.append(current_bankroll)
                bet_value_history.append(self.__bet_value)

            if self.__profit_or_lose(current_bankroll) > 0 and not (broke or stoploss_reached):
                profitors_count += 1
                profits.append(self.__profit_or_lose(current_bankroll))
            else:
                loses.append(self.__profit_or_lose(current_bankroll))

            if broke:
                broke_count += 1
            if stoploss_reached:
                sl_reached_count += 1
            if stopgain_reached:
                sg_reached_count += 1

            bankroll_histories.append(bankroll_history.copy())
            bet_value_histories.append(bet_value_history.copy())

        bet_count_histories = self.__get_bet_count_histories(bankroll_histories)

        Stats(self.bet_results, self.user_input, bankroll_histories,
              bet_value_histories, sl_reached_count, sg_reached_count,
              broke_count, profitors_count, profits, loses, self.title
        ).print_strategy_stats()

        graph.config(bet_count_histories, bankroll_histories, self.title)
        return graph

    # region BASE METHODS
    def __bet(self, bet_result, current_bankroll):
        if bet_result:
            current_bankroll += self.__bet_value*self.user_input['payout_rate']
        else:
            current_bankroll -= self.__bet_value
        return current_bankroll

    def __broke_verify(self, current_bankroll, broke, broken_when_is_less_than=1):
        if broken_when_is_less_than < 1:
            broken_when_is_less_than = 1

        if current_bankroll < broken_when_is_less_than:
            broke = True
        else:
            broke = False
        return broke

    def __stoploss_verify(self, current_bankroll, stoploss_reached):
        if self.user_input['stoploss'] is not None:
            if current_bankroll <= self.user_input['stoploss']:
                stoploss_reached = True
        return stoploss_reached

    def __stopgain_verify(self, current_bankroll, stopgain_reached):
        if self.user_input['stopgain'] is not None:
            if current_bankroll >= self.user_input['stopgain']:
                stopgain_reached = True
        return stopgain_reached

    def __profit_or_lose(self, current_bankroll):
        return current_bankroll - self.user_input['initial_bankroll']

    def __get_bet_count_histories(self, bankroll_histories):
        bet_count_histories = []
        for index, bankroll_history in enumerate(bankroll_histories):
            bet_count_histories.append(
                list(zip(*enumerate(bankroll_history, 1))))
            bet_count_histories[index] = list(bet_count_histories[index][0])
        return bet_count_histories
    # endregion

    # region BASE and HELPER METHODS
    def max_min_verify(self, bet_value):
        if self.user_input['minimum_bet_value'] is not None:
            if bet_value < self.user_input['minimum_bet_value']:
                bet_value = self.user_input['minimum_bet_value']
        if self.user_input['maximum_bet_value'] is not None:
            if bet_value > self.user_input['maximum_bet_value']:
                bet_value = self.user_input['maximum_bet_value']
        return bet_value
    # endregion

    # region HOOK METHODS
    def strategy_setup(self):
        """
        Strategy definitions, before everything starts
        """
        pass

    def bet_value_calculator_fixed(self):
        """
        Calculate the fixed amount of bet.
        """
        pass

    def bet_value_calculator_non_fixed(self):
        """
        Calculate the variable amount of bet, that can change every bet.
        """
        pass
    # endregion


class FixedBettor(Strategies):
    def __init__(
            self,
            bet_results: List[List[bool]],
            user_input: dict,
            title: str = 'Fixed Bettor',
            bet_value: Union[int, float, None] = None):
        super().__init__(bet_results, user_input, title)
        self.bet_value = bet_value

    def bet_value_calculator_fixed(self):
        if self.bet_value is None:
            self._Strategies__bet_value = self.user_input['bet_value']
        else:
            self._Strategies__bet_value = self.bet_value
        self._Strategies__bet_value = self.max_min_verify(
            self._Strategies__bet_value)


'''
def percentage_bettor(
    bet_results,
    user_input,
    title='Percentage Bettor',
    bet_percentage=None
) -> PlotGraph:

    if bet_percentage is None:
        bet_percentage = user_input['bet_percentage']

    for sample_result in bet_results:
        bankroll_history = [user_input['initial_bankroll']]
        bet_value_history = []
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
            bet_value_history.append(bet_value)

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
        bet_value_histories.append(bet_value_history.copy())
    bet_count_histories = bettor.get_bet_count_histories(bankroll_histories)

    print_strategy_stats(
        user_input, bankroll_histories, bet_value_histories, broke_count,
        sl_reached_count, sg_reached_count, profitors_count, profits, loses,
        title)

    graph.config(bet_count_histories, bankroll_histories, title)
    return graph


def kelly_criterion(
    bet_results,
    user_input,
    title='Kelly Criterion',
    kelly_fraction=1
) -> PlotGraph:

    kelly_percentage = user_input['win_rate'] - \
        ((1-user_input['win_rate'])/(user_input['payout_rate']/1))
    if kelly_percentage <= 0:
        print(f'\n*{title.upper()}*')
        print('Negative Expectation. DO NOT operate!')
        # FIXME the script are ploting an empty graph
        return [[], [], title]

    for sample_result in bet_results:
        bankroll_history = [user_input['initial_bankroll']]
        bet_value_history = []
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
            bet_value_history.append(bet_value)

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
        bet_value_histories.append(bet_value_history.copy())
    bet_count_histories = bettor.get_bet_count_histories(bankroll_histories)

    print_strategy_stats(
        user_input, bankroll_histories, bet_value_histories, broke_count,
        sl_reached_count, sg_reached_count, profitors_count, profits, loses, title, kelly_percentage)
    return bet_count_histories, bankroll_histories, title


def fixed_martingale(
    bet_results,
    user_input,
    title='Fixed Martingale',
    bet_value=None,
    multiplication_factor=2,
    round_limit=10,
    inverted=False
) -> PlotGraph:
    bettor = Bettor(user_input)

    current_round = 0
    sl_reached_count = 0
    sg_reached_count = 0
    broke_count = 0
    profitors_count = 0

    profits = []
    loses = []
    bet_count_histories = []
    bet_value_histories = []
    bankroll_histories = []

    if bet_value is None:
        bet_value = user_input['bet_value']
    bet_value = bettor.max_min_verify(bet_value)
    initial_bet_value = bet_value

    for sample_result in bet_results:
        bankroll_history = [user_input['initial_bankroll']]
        bet_value_history = []
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
            bet_value_history.append(bet_value)

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
        bet_value_histories.append(bet_value_history.copy())
    bet_count_histories = bettor.get_bet_count_histories(bankroll_histories)

    print_strategy_stats(
        user_input, bankroll_histories, bet_value_histories, broke_count,
        sl_reached_count, sg_reached_count, profitors_count, profits, loses, title)
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
) -> PlotGraph:
    bettor = Bettor(user_input)

    current_round = 0
    sl_reached_count = 0
    sg_reached_count = 0
    broke_count = 0
    profitors_count = 0

    profits = []
    loses = []
    bet_count_histories = []
    bet_value_histories = []
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
        bet_value_history = []
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
            bet_value_history.append(bet_value)

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
        bet_value_histories.append(bet_value_history.copy())
    bet_count_histories = bettor.get_bet_count_histories(bankroll_histories)

    if not use_kelly_percentage:
        print_strategy_stats(
            user_input, bankroll_histories, bet_value_histories, broke_count,
            sl_reached_count, sg_reached_count, profitors_count, profits, loses, title)
    else:
        print_strategy_stats(
            user_input, bankroll_histories, bet_value_histories, broke_count,
            sl_reached_count, sg_reached_count, profitors_count, profits, loses,
            title, kelly_percentage=bet_percentage)
    return bet_count_histories, bankroll_histories, title
'''
