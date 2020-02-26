from typing import Union, List
from abc import ABC, abstractmethod
from random import uniform

from betting.PlotGraph import PlotGraph
from betting.Stats import Stats
from betting.statistical_calculations import *
from betting.utils import *

"""
Strategies TODO: dAlembert, fibonacci,
oscars_grind, patrick, whittaker
"""
strategies_list = ['fixed_bettor', 'percentage_bettor', 'kelly_criterion',
                   'fixed_martingale', 'percentage_martingale', 'fixed_soros',
                   'percentage_soros']


class Strategies(ABC):
    def __init__(self, bet_results: List[List[bool]], user_input: dict, title: str):
        self.bet_results = bet_results
        self.user_input: dict = user_input
        self.title: str = title
        self.__bet_value = None

    def simulate_strategy(self):
        graph: PlotGraph = PlotGraph(self.user_input)

        self.__current_bankroll: Union[int, float] = self.user_input['initial_bankroll']
        self.__sample_result: List[bool] = self.bet_results[0][0]
        self.__bet_result_index: int = 0
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

        for self.__sample_result in self.bet_results:
            bankroll_history = [self.user_input['initial_bankroll']]
            bet_value_history = []
            self.__current_bankroll = self.user_input['initial_bankroll']
            for self.__bet_result_index, bet_result in enumerate(self.__sample_result):
                self.bet_value_calculator_non_fixed()
                self.__bet(bet_result)

                broke = self.__broke_verify(broke)
                stoploss_reached = self.__stoploss_verify(stoploss_reached)
                stopgain_reached = self.__stopgain_verify(stopgain_reached)
                if broke or stoploss_reached or stopgain_reached:
                    self.__current_bankroll = bankroll_history[-1]
                    break

                bankroll_history.append(self.__current_bankroll)
                bet_value_history.append(self.__bet_value)

            if self.__profit_or_lose() > 0 and not (broke or stoploss_reached):
                profitors_count += 1
                profits.append(self.__profit_or_lose())
            else:
                loses.append(self.__profit_or_lose())

            if broke: broke_count += 1
            if stoploss_reached: sl_reached_count += 1
            if stopgain_reached: sg_reached_count += 1

            bankroll_histories.append(bankroll_history.copy())
            bet_value_histories.append(bet_value_history.copy())

        bet_count_histories = self.__get_bet_count_histories(bankroll_histories)

        stats: Stats = Stats(self.bet_results, self.user_input, bankroll_histories,
                             bet_value_histories, sl_reached_count, sg_reached_count,
                             broke_count, profitors_count, profits, loses, self.title)

        stats.print_strategy_stats()
        graph.config(bet_count_histories, bankroll_histories, self.title)
        return graph

    # region BASE METHODS
    def __bet(self, bet_result):
        if bet_result: self.__current_bankroll += self.__bet_value*self.user_input['payout_rate']
        else: self.__current_bankroll -= self.__bet_value

    def __broke_verify(self, broke, broken_when_is_less_than=1):
        if broken_when_is_less_than < 1: broken_when_is_less_than = 1
        broke = True if self.__current_bankroll < broken_when_is_less_than else False
        return broke

    def __stoploss_verify(self, stoploss_reached):
        if self.user_input['stoploss'] is not None:
            if self.__current_bankroll <= self.user_input['stoploss']: stoploss_reached = True
        return stoploss_reached

    def __stopgain_verify(self, stopgain_reached):
        if self.user_input['stopgain'] is not None:
            if self.__current_bankroll >= self.user_input['stopgain']: stopgain_reached = True
        return stopgain_reached

    def __profit_or_lose(self):
        return self.__current_bankroll - self.user_input['initial_bankroll']

    def __get_bet_count_histories(self, bankroll_histories):
        bet_count_histories = []
        for index, bankroll_history in enumerate(bankroll_histories):
            bet_count_histories.append(list(zip(*enumerate(bankroll_history, 1))))
            bet_count_histories[index] = list(bet_count_histories[index][0])
        return bet_count_histories
    # endregion

    # region BASE and HELPER METHODS
    def max_min_verify(self, bet_value):
        if self.user_input['minimum_bet_value'] is not None:
            if bet_value < self.user_input['minimum_bet_value']: bet_value = self.user_input['minimum_bet_value']
        if self.user_input['maximum_bet_value'] is not None:
            if bet_value > self.user_input['maximum_bet_value']: bet_value = self.user_input['maximum_bet_value']
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
        if self.bet_value is None: self._Strategies__bet_value = self.user_input['bet_value']
        else: self._Strategies__bet_value = self.bet_value
        self._Strategies__bet_value = self.max_min_verify(self._Strategies__bet_value)


class PercentageBettor(Strategies):
    def __init__(
            self,
            bet_results: List[List[bool]],
            user_input: dict,
            title: str = 'Percentage Bettor',
            bet_percentage: Union[int, float, None] = None):
        super().__init__(bet_results, user_input, title)
        self.bet_percentage = bet_percentage

    def strategy_setup(self):
        if self.bet_percentage is None: self.bet_percentage = self.user_input['bet_percentage']

    def bet_value_calculator_non_fixed(self):
        self._Strategies__bet_value = self._Strategies__current_bankroll*self.bet_percentage
        self._Strategies__bet_value = self.max_min_verify(self._Strategies__bet_value)


class KellyCriterion(Strategies):
    def __init__(
            self,
            bet_results: List[List[bool]],
            user_input: dict,
            title: str = 'Kelly Criterion',
            kelly_fraction: Union[int, float, None] = 1):
        super().__init__(bet_results, user_input, title)
        self.kelly_fraction = kelly_fraction

    def strategy_setup(self):
        self.kelly_percentage = self.user_input['win_rate'] - ((1-self.user_input['win_rate']) / (self.user_input['payout_rate']/1))
        if self.kelly_percentage <= 0:
            print(f'\n*{self.title.upper()}*')
            print('Negative Expectation. DO NOT operate!')
            return [[], [], self.title]

    def bet_value_calculator_non_fixed(self):
        self._Strategies__bet_value = self._Strategies__current_bankroll * self.kelly_percentage*self.kelly_fraction
        self._Strategies__bet_value = self.max_min_verify(self._Strategies__bet_value)


class FixedMartingale(Strategies):
    def __init__(
            self,
            bet_results: List[List[bool]],
            user_input: dict,
            title: str = 'Fixed Martingale',
            bet_value: Union[int, float, None] = None,
            multiplication_factor: int = 2,
            round_limit: int = 5,
            inverted: bool = False):
        super().__init__(bet_results, user_input, title)
        self.bet_value = bet_value
        self.multiplication_factor = multiplication_factor
        self.round_limit = round_limit
        self.inverted = inverted

    def strategy_setup(self):
        if self.inverted and self.title == 'Fixed Martingale': self.title = 'Fixed Anti-Martingale'
        self.current_round = 0
    
    def bet_value_calculator_fixed(self):
        if self.bet_value is None: self._Strategies__bet_value = self.user_input['bet_value']
        self._Strategies__bet_value = self.max_min_verify(self._Strategies__bet_value)
        self.initial_bet_value = self._Strategies__bet_value

    def bet_value_calculator_non_fixed(self):
        expected_last_result = True if self.inverted else False
        previous_bet_result = self._Strategies__sample_result[self._Strategies__bet_result_index - 1]
        if previous_bet_result == expected_last_result and self._Strategies__bet_result_index > 0 and self.current_round < self.round_limit:
            self._Strategies__bet_value = self.multiplication_factor*self._Strategies__bet_value
            self._Strategies__bet_value = self.max_min_verify(self._Strategies__bet_value)
            self.current_round += 1
        else:
            self._Strategies__bet_value = self.initial_bet_value
            self.current_round = 0


class PercentageMartingale(Strategies):
    def __init__(
            self,
            bet_results: List[List[bool]],
            user_input: dict,
            title: str = 'Percentage Martingale',
            bet_percentage: Union[int, float, None] = None,
            multiplication_factor: int = 2,
            round_limit: int = 5,
            inverted: bool = False,
            use_kelly_percentage: bool = False,
            kelly_fraction: Union[int, float, None] = 1):
        super().__init__(bet_results, user_input, title)
        self.bet_percentage = bet_percentage
        self.multiplication_factor = multiplication_factor
        self.round_limit = round_limit
        self.inverted = inverted
        self.use_kelly_percentage = use_kelly_percentage
        self.kelly_fraction = kelly_fraction

    def strategy_setup(self):
        if self.inverted and self.use_kelly_percentage and self.title == 'Percentage Martingale':
            self.title = 'Percentage Kelly Anti-Martingale'
        elif self.inverted and not self.use_kelly_percentage and self.title == 'Percentage Martingale':
            self.title = 'Percentage Anti-Martingale'
        elif not self.inverted and self.use_kelly_percentage and self.title == 'Percentage Martingale':
            self.title = 'Percentage Kelly Martingale'

        self.current_round = 0
        if self.bet_percentage is None: self.bet_percentage = self.user_input['bet_percentage']
        if self.use_kelly_percentage:
            self.bet_percentage = self.user_input['win_rate'] - ((1-self.user_input['win_rate']) / (self.user_input['payout_rate']/1))
            if self.bet_percentage <= 0:
                print(f'\n*{self.title.upper()}*')
                print('Negative Expectation. DO NOT operate!')
                return [[], [], self.title]

    def bet_value_calculator_non_fixed(self):
        self.initial_bet_value = self._Strategies__current_bankroll*self.bet_percentage
        self.initial_bet_value = self.max_min_verify(self.initial_bet_value)

        expected_last_result = True if self.inverted else False
        previous_bet_result = self._Strategies__sample_result[self._Strategies__bet_result_index - 1]
        if previous_bet_result == expected_last_result and self._Strategies__bet_result_index > 0 and self.current_round < self.round_limit:
            self._Strategies__bet_value = self.multiplication_factor*self._Strategies__bet_value
            self._Strategies__bet_value = self.max_min_verify(self._Strategies__bet_value)
            self.current_round += 1
        else:
            self._Strategies__bet_value = self.initial_bet_value
            self.current_round = 0


class FixedSoros(Strategies):
    def __init__(
            self,
            bet_results: List[List[bool]],
            user_input: dict,
            title: str = 'Fixed Soros',
            bet_value: Union[int, float, None] = None,
            rounds: int = 5):
        super().__init__(bet_results, user_input, title)
        self.bet_value = bet_value
        self.round_limit = rounds
    
    def strategy_setup(self):
        if self.rounds <= 1: self.rounds = 2
        self.current_round = 0
    
    def bet_value_calculator_fixed(self):
        if self.bet_value is None: self._Strategies__bet_value = self.user_input['bet_value']
        self._Strategies__bet_value = self.max_min_verify(self._Strategies__bet_value)
        self.initial_bet_value = self._Strategies__bet_value

    def bet_value_calculator_non_fixed(self):
        previous_bet_result = self._Strategies__sample_result[self._Strategies__bet_result_index - 1]
        if previous_bet_result == True and self._Strategies__bet_result_index > 0 and self.current_round < self.round_limit:
            self._Strategies__bet_value += self._Strategies__bet_value*self.user_input['payout_rate']
            self._Strategies__bet_value = self.max_min_verify(self._Strategies__bet_value)
            self.current_round += 1
        else:
            self._Strategies__bet_value = self.initial_bet_value
            self.current_round = 0


class PercentageSoros(Strategies):
    def __init__(
            self,
            bet_results: List[List[bool]],
            user_input: dict,
            title: str = 'Percentage Soros',
            bet_percentage: Union[int, float, None] = None,
            rounds: int = 5,
            use_kelly_percentage: bool = False):
        super().__init__(bet_results, user_input, title)
        self.bet_percentage = bet_percentage
        self.round_limit = rounds
        self.use_kelly_percentage = use_kelly_percentage

    def strategy_setup(self):
        if self.rounds <= 1: self.rounds = 2
        self.current_round = 0

        if self.bet_percentage is None: self.bet_percentage = self.user_input['bet_percentage']
        if self.use_kelly_percentage:
            self.bet_percentage = self.user_input['win_rate'] - ((1-self.user_input['win_rate']) / (self.user_input['payout_rate']/1))
            if self.bet_percentage <= 0:
                print(f'\n*{self.title.upper()}*')
                print('Negative Expectation. DO NOT operate!')
                return [[], [], self.title]

    def bet_value_calculator_non_fixed(self):
        self.initial_bet_value = self._Strategies__current_bankroll*self.bet_percentage
        self.initial_bet_value = self.max_min_verify(self.initial_bet_value)

        previous_bet_result = self._Strategies__sample_result[self._Strategies__bet_result_index - 1]
        if previous_bet_result == True and self._Strategies__bet_result_index > 0 and self.current_round < self.round_limit:
            self._Strategies__bet_value += self._Strategies__bet_value*self.user_input['payout_rate']
            self._Strategies__bet_value = self.max_min_verify(self._Strategies__bet_value)
            self.current_round += 1
        else:
            self._Strategies__bet_value = self.initial_bet_value
            self.current_round = 0


class FixedFibonacci(Strategies):
    def __init__(
            self,
            bet_results: List[List[bool]],
            user_input: dict,
            title: str = 'Fixed Fibonacci',
            bet_value: Union[int, float, None] = None,
            round_limit: int = 5,
            inverted: bool = False):
        super().__init__(bet_results, user_input, title)
        self.bet_value = bet_value
        self.round_limit = round_limit
        self.inverted = inverted

    def strategy_setup(self):
        if self.inverted and self.title == 'Fixed Fibonacci': self.title = 'Fixed Anti-Fibonacci'
        self.current_round = 0
    
    def bet_value_calculator_fixed(self):
        if self.bet_value is None: self._Strategies__bet_value = self.user_input['bet_value']
        self._Strategies__bet_value = self.max_min_verify(self._Strategies__bet_value)
        self.initial_bet_value = self._Strategies__bet_value

    def bet_value_calculator_non_fixed(self):
        expected_last_result = True if self.inverted else False
        previous_bet_result = self._Strategies__sample_result[self._Strategies__bet_result_index - 1]
        if previous_bet_result == expected_last_result and self._Strategies__bet_result_index > 0 and self.current_round < self.round_limit:
            self._Strategies__bet_value = nth_fibonacci_number(self.current_round + 1)*self._Strategies__bet_value
            self._Strategies__bet_value = self.max_min_verify(self._Strategies__bet_value)
            self.current_round += 1
        else:
            self._Strategies__bet_value = self.initial_bet_value
            self.current_round = 0