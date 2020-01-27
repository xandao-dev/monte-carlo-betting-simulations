import matplotlib.pyplot as plt
import matplotlib.style as style
from typing import Union, List

style.use('bmh')

class PlotGraph:
    def __init__(self, bankroll: Union[int, float]) -> None:
        self.bankroll = bankroll
    
    def config(
            self,
            title: str,
            bet_count_history_X: List[List[int]],
            bankroll_history_Y: List[List[Union[int, float]]],
            new_fig: bool = True,
            color: Union[str, None] = None
    ) -> None:
        '''
        Parameters
        ----------
        title -> str
            The title of the graph.
        bet_count_history_X -> List[List[int]]
            bet_count_history_X is a list that contain the X axis lists which is
            the amount of bets.
        bankroll_history_Y -> List[List[Union[int, float]]]
            bankroll_history_Y is a list that contain the Y axis lists which is
            the bankroll history.
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
            for x, y in zip(bet_count_history_X, bankroll_history_Y):
                plt.plot(x, y, linewidth = 0.8)
            plt.title(title)
        elif not new_fig and color is None:
            for x, y in zip(bet_count_history_X, bankroll_history_Y):
                plt.plot(x, y, linewidth = 0.8)
        else:
            label_assigned = False
            for x, y in zip(bet_count_history_X, bankroll_history_Y):
                if not label_assigned:
                    plt.plot(x, y, linewidth = 0.8, label=title, color=color)
                    label_assigned = True
                plt.plot(x, y, linewidth = 0.8, color=color)
            leg = plt.legend()
            for line in leg.get_lines():
                line.set_linewidth(4.0)

        plt.ylabel('Bankroll')
        plt.xlabel('Bet Count')
        plt.axhline(self.bankroll, color = 'b', linewidth = 1.2)
        plt.axhline(0, color = 'r', linewidth = 1.2)

    def show(self) -> None:
        plt.show()