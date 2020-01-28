'''
Author: Alexandre Calil Martins Fonseca
https://github.com/xandao6/monte-carlo-betting-simulations

Credits: Oliver Wilkins
https://github.com/HomelessSandwich/MonteCarloBettingSim
''' 
from betting.strategies import fixed_bettor#, percentage_bettor, kelly_criterion
from betting.Bettor import Bettor
from betting.PlotGraph import PlotGraph
from typing import Union, List


# region USER INPUT
user_input = {
    'samples': 10,
    'bet_count': 10000,
    'win_rate': 0.5300,  # range: 0.0000-1.0000
    'payout_rate': 0.8700,  # range: 0.0000-2.0000 generally, but you choose
    'initial_bankroll': 1000,
    'currency': '$',
    'minimum_bet_value': None,
    'maximum_bet_value': None,
    'stoploss': None,
    'stopgain': None,
    #SPECIFIC INPUT
    'bet_value': 10,  # Fixed System
    'bet_percentage': 0.0100,  # Percentage System, range: 0.0000-1.0000
    'kelly_fraction': 1  # Kelly Criterion, range: 0.0000 to +inf, gen. 1 or 0.5
}
# endregion


def main():
    x, y = fixed_bettor(bet_results, user_input)
    plt.config('Fixed Bettor', x, y, new_fig=True, color='r')

    '''x, y = percentage_bettor(bet_results, user_input)
    plt.config('Percentage Bettor', x, y, new_fig=True, color='g')

    x, y = kelly_criterion(bet_results, user_input)
    plt.config('Kelly Criterion', x, y, new_fig=True, color='b')'''


if __name__ == '__main__':
    bet_results = Bettor.generate_random_bet_results(user_input)
    plt = PlotGraph(user_input['initial_bankroll'])
    main()
    plt.show()
