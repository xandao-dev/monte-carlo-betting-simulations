'''
This code is a modification of 
https://github.com/HomelessSandwich/MonteCarloBettingSim

HomelessSandwich/MonteCarloBettingSim is licensed under MIT
'''

from random import uniform
from typing import Union, List
'''
class Bettor:
    def __init__(self, initial_funds, colour):
        self.initial_funds = initial_funds
        self.funds = initial_funds
        self.colour = colour
        self.win_previous = True
        self.funds_history = []

    @staticmethod
    def bet_outcome():
        roll = round(random.uniform(0,1),4)
        if roll <= 50:
            return False
        else:
            return True

    @property
    def broke(self):
        if self.funds == 0:
            return True
        else:
            return False

    @property
    def profit(self):
        return self.funds - self.initial_funds

    def bet(self, wager):
        if self.funds < wager:
                wager = self.funds
        if self.bet_outcome():
            self.win_previous = True
            self.funds += wager
        else:
            self.win_previous = False
            self.funds -= wager
        self.plot_point()

    def plot_point(self):
        self.funds_history.append(self.funds)
'''


def generate_random_bet_results(general_input: dict) -> List[List[bool]]:
    '''
    Parameters
    ----------
    Returns
    -------
    List[List[bool]]
        The results are a list of betting results, the innermost lists
        represent the amount of bets and the outermost lists represent
        the number of samples.
    '''
    gi = general_input
    results = []
    for _ in range(gi['samples']):
        results_temp = []
        for _ in range(gi['bet_count']):
            result = round(uniform(0,1),4)
            if result <= gi['win_rate']:
                results_temp.append(True)
            elif result > gi['win_rate']:
                results_temp.append(False)
        results.append(results_temp.copy())
    return results