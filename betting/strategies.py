from typing import Union, Tuple, List
from random import uniform
from betting.PlotGraph import PlotGraph
from betting.UI import Stats
from betting.statistical_calculations import *
"""
Strategies TODO: dAlembert, fibonacci,
oscars_grind, patrick, sorogales, soros, whittaker
"""
strategies_list = ['fixed_bettor', 'percentage_bettor', 'kelly_criterion',
                   'fixed_martingale', 'percentage_martingale']


class Bettor:
    def __init__(self, user_input):
        self.user_input = user_input

    def generate_random_bet_results(self) -> List[List[bool]]:
        '''
        Parameters
        ----------
        Returns
        -------
        List[List[bool]]
            The bet_results are a list of betting results, the innermost lists
            represent the amount of bets and the outermost lists represent
            the number of samples.
        '''
        bet_results = []
        for _ in range(self.user_input['samples']):
            results_temp = []
            for _ in range(self.user_input['bet_count']):
                result = round(uniform(0, 1), 4)
                if result <= self.user_input['win_rate']:
                    results_temp.append(True)
                elif result > self.user_input['win_rate']:
                    results_temp.append(False)
            bet_results.append(results_temp.copy())
        return bet_results

    def profit(self, current_bankroll):
        return current_bankroll - self.user_input['initial_bankroll']

    def bet(self, bet_result, bet_value, current_bankroll):
        if bet_result:
            current_bankroll += bet_value*self.user_input['payout_rate']
        else:
            current_bankroll -= bet_value
        return current_bankroll

    def max_min_verify(self, bet_value):
        if self.user_input['minimum_bet_value'] is not None:
            if bet_value < self.user_input['minimum_bet_value']:
                bet_value = self.user_input['minimum_bet_value']
        if self.user_input['maximum_bet_value'] is not None:
            if bet_value > self.user_input['maximum_bet_value']:
                bet_value = self.user_input['maximum_bet_value']
        return bet_value

    def get_bet_count_histories(self, bankroll_histories):
        bet_count_histories = []
        for index, bankroll_history in enumerate(bankroll_histories):
            bet_count_histories.append(
                list(zip(*enumerate(bankroll_history, 1))))
            bet_count_histories[index] = list(bet_count_histories[index][0])
        return bet_count_histories


class Strategies():
    def __init__(self, user_input: dict, title: str):
        self.user_input: dict = user_input
        self.title: str = title

        self.sl_reached_count: int = 0
        self.sg_reached_count: int = 0
        self.broke_count: int = 0
        self.profitors_count: int = 0
        self.profits: List[Union[int, float]] = []
        self.loses: List[Union[int, float]] = []
        self.bet_count_histories: List[List[int]] = []
        self.bankroll_histories: List[List[Union[int, float]]] = []
        self.bet_value_histories: List[List[Union[int, float]]] = []

        self.broke: bool = False
        self.stoploss_reached: bool = False
        self.stopgain_reached: bool = False

        self.graph: PlotGraph = PlotGraph(self.user_input)
        self.bettor: Bettor = Bettor(self.user_input)
        self.bet_results = self.bettor.generate_random_bet_results()

        self.current_bankroll: Union[int, float] = self.user_input['initial_bankroll']
        self.bet_result = self.bet_results[0][0]
        self.bet_value = None

    def __stoploss_verify(self, current_bankroll):
        if self.user_input['stoploss'] is not None:
            if current_bankroll <= self.user_input['stoploss']:
                self.stoploss_reached = True

    def __stopgain_verify(self, current_bankroll):
        if self.user_input['stopgain'] is not None:
            if current_bankroll >= self.user_input['stopgain']:
                self.stopgain_reached = True

    def broke_verify(self, current_bankroll, broke_value=0):
        # On percentage systems we must use broke_value = 1
        if current_bankroll <= broke_value:
            self.broke = True
        else:
            self.broke = False

    def outsite_execution(self):
        """
        First function that runs inside simulate().
        """
        pass

    def first_loop_execution(self):
        """
        Second function that runs inside simulate(), after the first first 'for' loop.
        """
        pass

    def second_loop_execution(self):
        """
        Third function that runs inside simulate(), after the second 'for' loop.
        """
        pass

    def simulate(self):
        self.outsite_execution()

        for sample_result in self.bet_results:
            bankroll_history = [self.user_input['initial_bankroll']]
            bet_value_history = []
            self.current_bankroll = self.user_input['initial_bankroll']

            self.first_loop_execution()

            for self.bet_result in sample_result:
                self.second_loop_execution()

                #FIXME
                self.broke_verify(self.current_bankroll)

                self.__stoploss_verify(self.current_bankroll)
                self.__stopgain_verify(self.current_bankroll)
                if self.broke or self.stoploss_reached or self.stopgain_reached:
                    self.current_bankroll = bankroll_history[-1]
                    break

                bankroll_history.append(self.current_bankroll)
                bet_value_history.append(self.bet_value)

            if self.bettor.profit(self.current_bankroll) > 0 and not (self.broke or self.stoploss_reached):
                self.profitors_count += 1
                self.profits.append(self.bettor.profit(self.current_bankroll))
            else:
                self.loses.append(self.bettor.profit(self.current_bankroll))

            if self.broke:
                self.broke_count += 1
            if self.stoploss_reached:
                self.sl_reached_count += 1
            if self.stopgain_reached:
                self.sg_reached_count += 1

            self.bankroll_histories.append(bankroll_history.copy())
            self.bet_value_histories.append(bet_value_history.copy())

        bet_count_histories = self.bettor.get_bet_count_histories(
            self.bankroll_histories)

        #FIXME
        Stats(self.bet_results, self.user_input, self.bankroll_histories,
              self.bet_value_histories, self.sl_reached_count, self.sg_reached_count,
              self.broke_count, self.profitors_count, self.profits, self.loses, self.title
              ).print_strategy_stats()

        self.graph.config(bet_count_histories,
                          self.bankroll_histories, self.title)
        return self.graph


class FixedBettor(Strategies, Stats):
    def __init__(
            self,
            user_input: dict,
            title: str = 'Fixed Bettor',
            bet_value_fixed: Union[int, float, None] = None):
        super().__init__(user_input, title)
        self.bet_value_fixed = bet_value_fixed

    def outsite_execution(self):
        if self.bet_value_fixed is None:
            self.bet_value = self.user_input['bet_value']
        else: 
            self.bet_value = self.bet_value_fixed
        self.bet_value = self.bettor.max_min_verify(self.bet_value)

    def second_loop_execution(self):
        self.current_bankroll = self.bettor.bet(
            self.bet_result, self.bet_value, self.current_bankroll)

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
