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
            plot_bankroll_average: bool = True,
            new_fig: bool = True,
            color: Union[str, None] = None
    ) -> None:
        '''
        Parameters
        ----------
        title -> str
            The title of the graph.
        bet_count_histories -> List[List[int]]
            bet_count_histories is a list that contain the X axis lists which is
            the amount of bets.
        bankroll_histories -> List[List[Union[int, float]]]
            bankroll_histories is a list that contain the Y axis lists which is
            the bankroll history.
        plot_bankroll_average -> bool, optional
            Plot the banklroll average with a big width and red color.
        new_fig -> bool, optional
            new_fig is to open a new graph window. The default is True.
        color -> Union[str, None], optional
            The default is None.
        Returns
        -------
        None
        '''
        if new_fig:
            plt.figure()
            for x, y in zip(bet_count_histories, bankroll_histories):
                plt.plot(x, y, linewidth=0.8)
            plt.title(title)
        elif not new_fig and color is None:
            for x, y in zip(bet_count_histories, bankroll_histories):
                plt.plot(x, y, linewidth=0.8)
        else:
            label_assigned = False
            for x, y in zip(bet_count_histories, bankroll_histories):
                if not label_assigned:
                    plt.plot(x, y, linewidth=0.8, label=title, color=color)
                    label_assigned = True
                plt.plot(x, y, linewidth=0.8, color=color)
            leg = plt.legend()
            for line in leg.get_lines():
                line.set_linewidth(4.0)
        #FIXME
        if plot_bankroll_average:
            bankroll_history_average = self.__get_bankroll_history_average(
                bankroll_histories)
            bet_count_history = self.__get_bet_count_history(
                bankroll_history_average)
            plt.plot(bet_count_history, bankroll_history_average, linewidth=2, color='r')

        plt.ylabel('Bankroll')
        plt.xlabel('Bet Count')
        plt.axhline(self.user_input['initial_bankroll'],
                    color='b', linewidth=1.2)
        plt.axhline(0, color='r', linewidth=1.2)

    def __get_bankroll_history_average(self, bankroll_histories):
        bankroll_history_sum = []
        bankroll_history_average = []
        for i, bankroll_history in enumerate(bankroll_histories):
            for j, bankroll in enumerate(bankroll_history):
                if i == 0:
                    bankroll_history_sum.append(bankroll)
                else:
                    bankroll_history_sum[j] += bankroll
        for bankroll in bankroll_history_sum:
            bankroll_history_average.append(
                bankroll/self.user_input['samples'])
        return bankroll_history_average

    def __get_bet_count_history(self, bankroll_history_average):
        bet_count_history = []
        bet_count_history.append(
            list(zip(*enumerate(bankroll_history_average, 1))))
        bet_count_history = list(bet_count_history[0])
        return bet_count_history

    def show(self) -> None:
        plt.show()
