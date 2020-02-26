'''
Author: Alexandre Calil Martins Fonseca
https://github.com/xandao6/monte-carlo-betting-simulations
'''

from betting.BetGenerator import BetGenerator
from betting.Strategies import FixedBettor, PercentageBettor, KellyCriterion, FixedMartingale
from betting.Strategies import PercentageMartingale, FixedSoros, PercentageSoros, FixedFibonacci
from betting.Strategies import PercentageFibonacci
from betting.PlotGraph import PlotGraph
from betting.Stats import Stats


user_input = {
    'samples': 100,
    'bet_count': 1000,
    'win_rate': 0.5500,  # range: 0.0000-1.0000
    'lose_rate': 0.4500,  # range: 1.0000-0.0000
    'payout_rate': 0.8700,  # range: 0.0000-2.0000 generally, but you choose
    'initial_bankroll': 250,
    'currency': '$',
    'minimum_bet_value': 2,
    'maximum_bet_value': None,
    'stoploss': None,
    'stopgain': None,
    'bet_value': 5, # Isn't used in all strategies
    'bet_percentage': 0.0100,  # Isn't used in all strategies, range: 0.0000-1.0000
}

bet_results = BetGenerator(user_input).generate_random_bet_results()
data = (bet_results, user_input)


def main():
    # Stats.print_indicators_tutorial('PORTUGUESE')
    Stats(user_input=user_input).print_general_stats()

    #FixedBettor(*data).simulate_strategy()
    #PercentageBettor(*data).simulate_strategy()
    KellyCriterion(*data).simulate_strategy()
    #FixedMartingale(*data).simulate_strategy()
    #FixedMartingale(*data, inverted=True).simulate_strategy()
    #PercentageMartingale(*data).simulate_strategy()
    #PercentageMartingale(*data, use_kelly_percentage=True).simulate_strategy()
    #PercentageMartingale(*data, inverted=True).simulate_strategy()
    #PercentageMartingale(*data, inverted=True, use_kelly_percentage=True).simulate_strategy()
    #FixedSoros(*data).simulate_strategy()
    #PercentageSoros(*data).simulate_strategy()
    #PercentageSoros(*data, use_kelly_percentage=True).simulate_strategy()
    #PercentageSoros(*data, inverted=True).simulate_strategy()
    #PercentageSoros(*data, inverted=True, use_kelly_percentage=True).simulate_strategy()
    #FixedFibonacci(*data).simulate_strategy()
    #FixedFibonacci(*data, inverted=True).simulate_strategy()
    #PercentageFibonacci(*data).simulate_strategy()
    #PercentageFibonacci(*data, use_kelly_percentage=True).simulate_strategy()
    #PercentageFibonacci(*data, inverted=True).simulate_strategy()
    #PercentageFibonacci(*data, inverted=True, use_kelly_percentage=True).simulate_strategy()

    # YOU CAN USE FOR LOOPS TO CHANGE PARAMETERS
    #for i in range(2,7,2):
    #    FixedSoros(*data, title=f'Fixed Soros, round max: {i}', rounds=i).simulate_strategy()

    PlotGraph.show()


if __name__ == '__main__':
    main()
