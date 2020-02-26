import matplotlib.pyplot as plt
import matplotlib.style as style
from typing import Union, List

from betting.utils import *
style.use('bmh')


class PlotGraph:
    def __init__(self, user_input: dict) -> None:
        self.user_input = user_input

    def config(
            self,
            bet_count_histories: List[List[int]],
            bankroll_histories: List[List[Union[int, float]]],
            title: str,
    ) -> None:
        plt.figure()
        [plt.plot(x, y, linewidth=0.8)
         for x, y in zip(bet_count_histories, bankroll_histories)]
        plt.title(title)

        if self.user_input['samples'] > 1:
            self.__config_bankroll_average(bankroll_histories)

        plt.ylabel('Bankroll')
        plt.xlabel('Bet Count')
        plt.axhline(self.user_input['initial_bankroll'],
                    color='b', linewidth=1.2)
        plt.axhline(0, color='r', linewidth=1.2)

    def __config_bankroll_average(self, bankroll_histories):
        bankroll_history_average = get_bankroll_history_average(user_input['samples'], bankroll_histories)
        bet_count_history = get_bet_count_history(bankroll_history_average)
        plt.plot(bet_count_history, bankroll_history_average,
                 linewidth=2.5, color='k', label='Bankroll Average')
        leg = plt.legend(loc='upper left')
        [line.set_linewidth(4.0) for line in leg.get_lines()]

    @staticmethod
    def show() -> None:
        plt.show()
