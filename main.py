'''
Author: Alexandre Calil Martins Fonseca
https://github.com/xandao6/monte-carlo-betting-simulations

Credits: Oliver Wilkins
https://github.com/HomelessSandwich/MonteCarloBettingSim
'''
from betting.strategies import fixed_bettor, percentage_bettor, kelly_criterion
from betting.strategies import fixed_martingale
from betting.Bettor import Bettor
from betting.PlotGraph import PlotGraph
from typing import Union, List


# region USER INPUT
user_input = {
    'samples': 250,
    'bet_count': 5000,
    'win_rate': 0.5500,  # range: 0.0000-1.0000
    'payout_rate': 0.8500,  # range: 0.0000-2.0000 generally, but you choose
    'initial_bankroll': 1000,
    'currency': '$',
    'minimum_bet_value': None,
    'maximum_bet_value': None,
    'stoploss': None,
    'stopgain': None,
    # SPECIFIC INPUT
    'bet_value': 10,  # Fixed System
    'bet_percentage': 0.0100,  # Percentage System, range: 0.0000-1.0000
    }
# endregion


def main():
    data = fixed_bettor(bet_results, user_input)
    plt.config(*data, new_fig=True, color='r')

    data = percentage_bettor(bet_results, user_input)
    plt.config(*data, new_fig=True, color='g')

    data = kelly_criterion(bet_results, user_input)
    plt.config(*data, new_fig=True, color='b')

    data = fixed_martingale(bet_results, user_input, title='MG Normal')
    plt.config(*data, new_fig=True, color='c')
    
    data = fixed_martingale(bet_results, user_input, title='Anti-MG', inverted=True)
    plt.config(*data, new_fig=True, color='c')

if __name__ == '__main__':
    bet_results = Bettor.generate_random_bet_results(user_input)
    plt = PlotGraph(user_input['initial_bankroll'])
    main()
    plt.show()
