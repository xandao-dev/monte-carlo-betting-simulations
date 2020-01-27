'''
Author: Alexandre Calil Martins Fonseca
https://github.com/xandao6/monte-carlo-betting-simulations

Credits: Oliver Wilkins
https://github.com/HomelessSandwich/MonteCarloBettingSim
'''
from betting.strategies import StrategiesData
from betting.strategies import fixed_bettor, percentage_bettor, kelly_criterion
from betting.Bettor import generate_random_bet_results
from betting.PlotGraph import PlotGraph
from typing import Union, List


# region USER INPUT
general_input = {
    'samples': 10,
    'bet_count': 10000,
    'win_rate': 0.5600,  # range: 0.0000-1.0000
    'payout_rate': 0.8700,  # range: 0.0000-2.0000 generally, but you choose
    'bankroll': 1000,
    'currency': '$',
    'minimum_bet_value': None,
    'maximum_bet_value': None,
    'stoploss': None,
    'stopgain': None
}
specific_input = {
    'bet_value': 10,  # Fixed System
    'bet_percentage': 0.0100,  # Percentage System, range: 0.0000-1.0000
    'kelly_fraction': 1  # Kelly Criterion, range: 0.0000 to +inf, gen. 1 or 0.5
}
# endregion


def main():
    bet_results = generate_random_bet_results(general_input)
    data = StrategiesData(bet_results, general_input, specific_input)
    plt = PlotGraph(general_input['bankroll'])

    betX, bkrY = fixed_bettor(data)
    plt.config('Fixed System', betX, bkrY, new_fig=True, color='r')

    betX, bkrY = percentage_bettor(data)
    plt.config('Percentage System', betX, bkrY, new_fig=True, color='g')

    betX, bkrY = kelly_criterion(data)
    plt.config('Kelly Criterion', betX, bkrY, new_fig=True, color='b')

    plt.show()


if __name__ == '__main__':
    main()
