__author__ = 'Alexandre Calil Martins Fonseca, Github: xandao6'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# FIXME Ideia: poder comparar medias
# FIXME Ideia: ver bankroll maximo
# FIXME Ideia: melhor sistema (bankroll average * survival rate)

from strategies.fixed_system import fixed_system
from strategies.percentage_system import percentage_system
from strategies.kelly_criterion import kelly_criterion
from typing import Union, List
import random
import matplotlib.pyplot as plt
import matplotlib.style as style


style.use('bmh')

#region USER INPUT
# General Input
samples = 10
bet_count = 100000
win_rate = 0.4857 # win rate: 0.0000-1.0000
payout_rate = 1.0000 # payout rate: 0.0000-2.0000 generally, but you choose
bankroll = 1000
minimum_bet_value = None
maximum_bet_value = None
stoploss = None
stopgain = None

#Fixed System Input
bet_value = 10

#Percentage System Input
bet_percentage = 0.0100 # bet percentage: 0.0000-1.0000

# Kelly Criterion Input
kelly_fraction = 1 # kelly fraction: 0.0000 to +inf, generally 1, 0.5 or 0.25
#endregion

def main():
    results = generate_random_bet_results(win_rate, bet_count, samples)

    betX, bkrY = fixed_system(
        results,
        payout_rate,
        bankroll,
        bet_value,
        minimum_bet_value,
        maximum_bet_value,
        stoploss,
        stopgain)
    plot_config('Fixed System', betX, bkrY, True, 'r')

    betX, bkrY = percentage_system(
        results,
        payout_rate,
        bankroll,
        bet_percentage,
        minimum_bet_value,
        maximum_bet_value,
        stoploss,
        stopgain)
    plot_config('Percentage System', betX, bkrY, True, 'g')

    betX, bkrY = kelly_criterion(
        results,
        win_rate,
        payout_rate,
        bankroll,
        kelly_fraction,
        minimum_bet_value,
        maximum_bet_value,
        stoploss,
        stopgain)
    plot_config('Kelly Criterion', betX, bkrY, True, 'b')

    plt.show()


def generate_random_bet_results(
        win_rate: float,
        bet_count: int,
        samples: int
) -> List[List[bool]]:
    '''
    Parameters
    ----------
    win_rate -> float
        The win rate is a rate that can range from 0.0000 to 1.0000, which
        means the percentage you have of winning.
        To know your win rate you must divide the total bets you won by the
        total bet, the more bets the more
        accurate that rate will be.
    bet_count -> int
        The bet count is the amount of bets you will simulate.
    samples -> int
        The amount of samples that we will plot on the graph.

    Returns
    -------
    List[List[bool]]
        The results are a list of betting results, the innermost lists
        represent the amount of bets and the outermost lists represent
        the number of samples.
    '''
    results = []
    for _ in range(samples):
        results_temp = []
        for _ in range(bet_count):
            result = round(random.uniform(0,1),4)
            if result <= win_rate:
                results_temp.append(True)
            elif result > win_rate:
                results_temp.append(False)
        results.append(results_temp.copy())
    return results


def plot_config(
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
    plt.axhline(bankroll, color = 'b', linewidth = 0.5)
    plt.axhline(0, color = 'r', linewidth = 2)


if __name__ == '__main__':
    main()