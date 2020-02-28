import unittest

import betting
from betting.Strategies import FixedBettor, PercentageBettor, KellyCriterion, FixedMartingale
from betting.Strategies import PercentageMartingale, FixedSoros, PercentageSoros, FixedFibonacci
from betting.Strategies import PercentageFibonacci, FixedDAlembert


user_input = {
    'samples': 6,
    'bet_count': 6,
    'win_rate': 0.5000,
    'lose_rate': 0.5000,
    'payout_rate': 0.5000,
    'initial_bankroll': 1000,
    'currency': '$',
    'minimum_bet_value': None,
    'maximum_bet_value': None,
    'stoploss': None,
    'stopgain': None,
    'bet_value': 10,
    'bet_percentage': 0.0100,
}

bet_results = [
    [True]*6,
    [False]*6,
    [True, False]*3,
    [False, True]*3,
    [False, False, False, True, True, True],
    [True, True, True, False, False, False]
]


class TestFixedBettor(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """
        expected_bet_value_histories = [[10]*6]*6

        fb = FixedBettor(bet_results, user_input)
        fb.simulate_strategy()
        [print(bv) for bv in fb.bet_value_histories]
        self.assertEqual(fb.bet_value_histories, expected_bet_value_histories)


class TestPercentageBettor(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """

        expected_bet_value_histories = [
            [10, 10.05, 10.10, 10.15, 10.20, 10.25],
            [10, 9.90, 9.80, 9.70, 9.61, 9.51],
            [10, 10.05, 9.95, 10.00, 9.90, 9.95],
            [10, 9.90, 9.95, 9.85, 9.90, 9.80],
            [10, 9.90, 9.80, 9.70, 9.75, 9.80],
            [10, 10.05, 10.1, 10.15, 10.05, 9.95]
        ]

        pb = PercentageBettor(bet_results, user_input)
        pb.simulate_strategy()
        [print(bv) for bv in pb.bet_value_histories]
        self.assertEqual(pb.bet_value_histories, expected_bet_value_histories)

'''
class TestKellyCriterion(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        ""

        expected_bet_value_histories = [
            [155.56, 177.33, 202.16, 230.46, 262.73, 299.51],
            [155.56, 131.36, 110.92, 93.67, 79.1, 66.79],
            [155.56, 177.33, 149.75, 170.71, 144.16, 164.34],
            [155.56, 131.36, 149.75, 126.45, 144.16, 121.73],
            [155.56, 131.36, 110.92, 93.67, 106.78, 121.73],
            [155.56, 177.33, 202.16, 230.46, 194.61, 164.34]
        ]

        kc = KellyCriterion(bet_results, user_input)
        kc.simulate_strategy()
        [print(bv) for bv in kc.bet_value_histories]
        #self.assertEqual(kc.bet_value_histories, expected_bet_value_histories)
'''

if __name__ == '__main__':
    unittest.main()
