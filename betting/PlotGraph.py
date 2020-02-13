import matplotlib.pyplot as plt
import matplotlib.style as style
from typing import Union, List
style.use('bmh')


class PlotGraph:
    def __init__(self, user_input: dict) -> None:
        self.user_input = user_input

    def config(
            self,
            bet_count_histories: List[List[int]],
            bankroll_histories: List[List[Union[int, float]]],
            title: str,
            plot_bankroll_average: bool = True
    ) -> None:
        plt.figure()
        [plt.plot(x, y, linewidth=0.8)
         for x, y in zip(bet_count_histories, bankroll_histories)]
        plt.title(title)

        if plot_bankroll_average:
            self.__config_bankroll_average(bankroll_histories)

        plt.ylabel('Bankroll')
        plt.xlabel('Bet Count')
        plt.axhline(self.user_input['initial_bankroll'],
                    color='b', linewidth=1.2)
        plt.axhline(0, color='r', linewidth=1.2)

    def __config_bankroll_average(self, bankroll_histories):
        bankroll_history_average = self.__get_bankroll_history_average(
            bankroll_histories)
        bet_count_history = self.__get_bet_count_history(
            bankroll_history_average)
        plt.plot(bet_count_history, bankroll_history_average,
                 linewidth=2.5, color='k', label='Bankroll Average')
        leg = plt.legend()
        [line.set_linewidth(4.0) for line in leg.get_lines()]

    def __get_bankroll_history_average(self, bankroll_histories):
        bankroll_history_sum = []
        bankroll_history_average = []
        for i, bankroll_history in enumerate(bankroll_histories):
            for j, bankroll in enumerate(bankroll_history):
                if i == 0:
                    bankroll_history_sum.append(bankroll)
                else:
                    try:
                        bankroll_history_sum[j] += bankroll
                    except IndexError:
                        bankroll_history_sum.append(bankroll)

        for bankroll in bankroll_history_sum:
            bankroll_history_average.append(
                bankroll/self.user_input['samples'])
        return bankroll_history_average

    def __get_bet_count_history(self, bankroll_history_average):
        try:
            bet_count_history = list(
                zip(*enumerate(bankroll_history_average, 1)))[0]
        except IndexError:
            return list()
        return bet_count_history

    def show(self) -> None:
        plt.show()
