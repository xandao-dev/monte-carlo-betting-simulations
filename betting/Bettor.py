'''
This code is a modification of 
https://github.com/HomelessSandwich/MonteCarloBettingSim

HomelessSandwich/MonteCarloBettingSim is licensed under MIT
'''

from random import uniform
from typing import Union, List


class Bettor:
    def __init__(self, user_input):
        self.user_input = user_input
        self.funds_history = []

    @staticmethod
    def generate_random_bet_results(user_input: dict) -> List[List[bool]]:
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
        for _ in range(user_input['samples']):
            results_temp = []
            for _ in range(user_input['bet_count']):
                result = round(uniform(0, 1), 4)
                if result <= user_input['win_rate']:
                    results_temp.append(True)
                elif result > user_input['win_rate']:
                    results_temp.append(False)
            bet_results.append(results_temp.copy())
        return bet_results

    def max_min_verify(self, bet_value):
        if self.user_input['minimum_bet_value'] is not None:
            if bet_value < self.user_input['minimum_bet_value']:
                bet_value = self.user_input['minimum_bet_value']
        if self.user_input['maximum_bet_value'] is not None:
            if bet_value > self.user_input['maximum_bet_value']:
                bet_value = self.user_input['maximum_bet_value']
        return bet_value

    def stoploss_verify(self, current_bankroll):
        stoploss_reached = False
        if self.user_input['stoploss'] is not None:
            if current_bankroll <= self.user_input['stoploss']:
                stoploss_reached = True
        return stoploss_reached

    def stopgain_verify(self, current_bankroll):
        stopgain_reached = False
        if self.user_input['stopgain'] is not None:
            if current_bankroll >= self.user_input['stopgain']:
                stopgain_reached = True
        return stopgain_reached

    def broke_verify(self, current_bankroll, broke_value = 0):
        #On percentage systems we must use broke_value = 1
        if current_bankroll <= broke_value:
            broke = True
        else:
            broke = False
        return broke

    def profit(self, current_bankroll):
        return current_bankroll - self.user_input['initial_bankroll']

    def bet(self, bet_result, bet_value, current_bankroll):
        if bet_result:
            current_bankroll += bet_value*self.user_input['payout_rate']
        else:
            current_bankroll -= bet_value
        return current_bankroll

    def get_bet_count_histories(self, bankroll_histories):
        bet_count_histories = []
        for index, bankroll_history in enumerate(bankroll_histories):
            bet_count_histories.append(
                list(zip(*enumerate(bankroll_history, 1))))
            bet_count_histories[index] = list(bet_count_histories[index][0])
        return bet_count_histories
