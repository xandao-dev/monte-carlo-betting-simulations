'''
Author: Alexandre Calil Martins Fonseca
https://github.com/xandao6/monte-carlo-betting-simulations

Credits: Oliver Wilkins
https://github.com/HomelessSandwich/MonteCarloBettingSim
'''
from betting.strategies import fixed_bettor, percentage_bettor, kelly_criterion
from betting.strategies import fixed_martingale, percentage_martingale
from betting.Bettor import Bettor
from betting.PlotGraph import PlotGraph
from betting.ui import print_indicators_tutorial, print_general_stats
from typing import Union, List


# region USER INPUT
user_input = {
    'samples': 250,
    'bet_count': 2500,
    'win_rate': 0.5500,  # range: 0.0000-1.0000
    'lose_rate': 0.4500, # range: 1.0000-0.0000
    'payout_rate': 0.9000,  # range: 0.0000-2.0000 generally, but you choose
    'initial_bankroll': 10000,
    'currency': '$',
    'minimum_bet_value': None,
    'maximum_bet_value': None,
    'stoploss': None,
    'stopgain': None,
    # SPECIFIC INPUT
    'bet_value': 10,  # Fixed System and MG
    'bet_percentage': 0.0100,  # Percentage System and MG, range: 0.0000-1.0000
}
# endregion


def main():
    #print_indicators_tutorial('PORTUGUESE')
    print_general_stats(bet_results, user_input)

    data = fixed_bettor(bet_results, user_input)
    plt.config(*data, user_input)

    #data = percentage_bettor(bet_results, user_input)
    #plt.config(*data, user_input)

    data = kelly_criterion(bet_results, user_input)
    plt.config(*data, user_input)

    #data = fixed_martingale(bet_results, user_input)
    #plt.config(*data, user_input)

    #data = fixed_martingale(bet_results, user_input, inverted=True,
    #                        title='Fixed Anti-Martingale')
    #plt.config(*data, user_input)

    #data = percentage_martingale(bet_results, user_input)
    #plt.config(*data, user_input)

    #data = percentage_martingale(bet_results, user_input, inverted=True,
    #                             title='Percentage Anti-Martingale')
    #plt.config(*data, user_input)

    plt.show()# Show Graphs


if __name__ == '__main__':
    bet_results = Bettor.generate_random_bet_results(user_input)
    plt = PlotGraph(user_input)
    main()
