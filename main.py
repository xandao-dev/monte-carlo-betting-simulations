'''
Author: Alexandre Calil Martins Fonseca
https://github.com/xandao6/monte-carlo-betting-simulations
'''
from betting.strategies import FixedBettor
from betting.PlotGraph import PlotGraph
from betting.UI import Stats
from typing import Union, List


user_input = {
    'samples': 10,
    'bet_count': 5000,
    'win_rate': 0.5500,  # range: 0.0000-1.0000
    'lose_rate': 0.4500,  # range: 1.0000-0.0000
    'payout_rate': 0.8700,  # range: 0.0000-2.0000 generally, but you choose
    'initial_bankroll': 250,
    'currency': '$',
    'minimum_bet_value': None,
    'maximum_bet_value': None,
    'stoploss': None,
    'stopgain': None,
    # SPECIFIC INPUT
    'bet_value': 5,  # Fixed System and MG
    'bet_percentage': 0.0100,  # Percentage System and MG, range: 0.0000-1.0000
}


def main():
    # Stats().print_indicators_tutorial('PORTUGUESE')
    Stats(user_input=user_input).print_general_stats()

    FixedBettor(user_input).simulate().show()
    #fixed_bettor(bet_results, user_input).show()
    #percentage_bettor(bet_results, user_input).show()


'''
    kelly_criterion(bet_results, user_input).show()

    fixed_martingale(bet_results, user_input, round_limit=3).show()

    fixed_martingale(bet_results, user_input, inverted=True,
                     title='Fixed Anti-Martingale', 
                     round_limit=3).show()

    percentage_martingale(bet_results, user_input, round_limit=3)

    percentage_martingale(bet_results, user_input, inverted=True,
                                 title='Percentage Anti-Martingale',
                                 round_limit=3).show()
'''

if __name__ == '__main__':
    main()
