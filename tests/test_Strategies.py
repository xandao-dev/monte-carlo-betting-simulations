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

'''
class TestFixedBettor(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """
        user_input['win_rate'] = 0.5000
        user_input['lose_rate'] = 0.5000
        user_input['payout_rate'] = 0.5000

        expected_bet_value_histories = [[10]*6]*6

        fb = FixedBettor(bet_results, user_input)
        fb.simulate_strategy()
        #[print(bv) for bv in fb.bet_value_histories]
        self.assertEqual(fb.bet_value_histories, expected_bet_value_histories)


class TestPercentageBettor(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """
        user_input['win_rate'] = 0.5000
        user_input['lose_rate'] = 0.5000
        user_input['payout_rate'] = 0.5000

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
        #[print(bv) for bv in pb.bet_value_histories]
        self.assertEqual(pb.bet_value_histories, expected_bet_value_histories)


class TestKellyCriterion(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """
        user_input['win_rate'] = 0.6000
        user_input['lose_rate'] = 0.4000
        user_input['payout_rate'] = 0.9000

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
        #[print(bv) for bv in kc.bet_value_histories]
        self.assertEqual(kc.bet_value_histories, expected_bet_value_histories)


class TestFixedMartingale(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """
        user_input['win_rate'] = 0.5000
        user_input['lose_rate'] = 0.5000
        user_input['payout_rate'] = 0.5000

        # region normal mode
        expected_bet_value_histories = [
            [10, 10, 10, 10, 10, 10],
            [10, 20, 40, 80, 160, 320],
            [10, 10, 20, 10, 20, 10],
            [10, 20, 10, 20, 10, 20],
            [10, 20, 40, 80, 10, 10],
            [10, 10, 10, 10, 20, 40]
        ]
        mg = FixedMartingale(bet_results, user_input,)
        mg.simulate_strategy()
        #[print(bv) for bv in mg.bet_value_histories]
        self.assertEqual(mg.bet_value_histories, expected_bet_value_histories)
        # endregion

        # region multiplication factor and round limit mode
        expected_bet_value_histories = [
            [10, 10, 10, 10, 10, 10],
            [10, 25, 62.5, 10, 25, 62.5],
            [10, 10, 25, 10, 25, 10],
            [10, 25, 10, 25, 10, 25],
            [10, 25, 62.5, 10, 10, 10],
            [10, 10, 10, 10, 25, 62.5]
        ]
        mg = FixedMartingale(bet_results, user_input, multiplication_factor=2.5, round_limit=2)
        mg.simulate_strategy()
        #[print(bv) for bv in mg.bet_value_histories]
        self.assertEqual(mg.bet_value_histories, expected_bet_value_histories)
        # endregion

        # region inverded mode
        expected_bet_value_histories = [
            [10, 20, 40, 80, 160, 320],
            [10, 10, 10, 10, 10, 10],
            [10, 20, 10, 20, 10, 20],
            [10, 10, 20, 10, 20, 10],
            [10, 10, 10, 10, 20, 40],
            [10, 20, 40, 80, 10, 10]
        ]
        mg = FixedMartingale(bet_results, user_input, inverted=True)
        mg.simulate_strategy()
        #[print(bv) for bv in mg.bet_value_histories]
        self.assertEqual(mg.bet_value_histories, expected_bet_value_histories)
        # endregion

        # region inverted mode with multiplication factor and round limit
        expected_bet_value_histories = [
            [10, 25, 62.5, 10, 25, 62.5],
            [10, 10, 10, 10, 10, 10],
            [10, 25, 10, 25, 10, 25],
            [10, 10, 25, 10, 25, 10],
            [10, 10, 10, 10, 25, 62.5],
            [10, 25, 62.5, 10, 10, 10]
        ]
        mg = FixedMartingale(bet_results, user_input, inverted=True, multiplication_factor=2.5, round_limit=2)
        mg.simulate_strategy()
        #[print(bv) for bv in mg.bet_value_histories]
        self.assertEqual(mg.bet_value_histories, expected_bet_value_histories)
        # endregion


class TestPercentageMartingale(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """
        user_input['win_rate'] = 0.5000
        user_input['lose_rate'] = 0.5000
        user_input['payout_rate'] = 0.5000

        # region normal mode
        expected_bet_value_histories = [
            [10.0, 10.05, 10.1, 10.15, 10.2, 10.25],
            [10.0, 20.0, 40.0, 80.0, 160.0, 320.0],
            [10.0, 10.05, 20.1, 10.05, 20.1, 10.05],
            [10.0, 20.0, 10.0, 20.0, 10.0, 20.0],
            [10.0, 20.0, 40.0, 80.0, 9.7, 9.75],
            [10.0, 10.05, 10.1, 10.15, 20.3, 40.6]
        ]
        mg = PercentageMartingale(bet_results, user_input,)
        mg.simulate_strategy()
        #[print(bv) for bv in mg.bet_value_histories]
        self.assertEqual(mg.bet_value_histories, expected_bet_value_histories)
        # endregion

        # region multiplication factor and round limit mode
        expected_bet_value_histories = [
            [10.0, 10.05, 10.1, 10.15, 10.2, 10.25],
            [10.0, 25.0, 62.5, 9.03, 22.57, 56.42],
            [10.0, 10.05, 25.12, 10.08, 25.2, 10.1],
            [10.0, 25.0, 10.03, 25.07, 10.05, 25.12],
            [10.0, 25.0, 62.5, 9.03, 9.07, 9.12],
            [10.0, 10.05, 10.1, 10.15, 25.38, 63.45]
        ]
        mg = PercentageMartingale(bet_results, user_input, multiplication_factor=2.5, round_limit=2)
        mg.simulate_strategy()
        #[print(bv) for bv in mg.bet_value_histories]
        self.assertEqual(mg.bet_value_histories, expected_bet_value_histories)
        # endregion

        # region inverded mode
        expected_bet_value_histories = [
            [10.0, 20.0, 40.0, 80.0, 160.0, 320.0],
            [10.0, 9.9, 9.8, 9.7, 9.61, 9.51],
            [10.0, 20.0, 9.85, 19.7, 9.7, 19.4],
            [10.0, 9.9, 19.8, 9.75, 19.5, 9.61],
            [10.0, 9.9, 9.8, 9.7, 19.4, 38.8],
            [10.0, 20.0, 40.0, 80.0, 9.55, 9.45]
        ]
        mg = PercentageMartingale(bet_results, user_input, inverted=True)
        mg.simulate_strategy()
        #[print(bv) for bv in mg.bet_value_histories]
        self.assertEqual(mg.bet_value_histories, expected_bet_value_histories)
        # endregion

        # region inverted mode with multiplication factor and round limit
        expected_bet_value_histories = [
            [10.0, 25.0, 62.5, 10.49, 26.23, 65.58],
            [10.0, 9.9, 9.8, 9.7, 9.61, 9.51],
            [10.0, 25.0, 9.8, 24.5, 9.6, 24.0],
            [10.0, 9.9, 24.75, 9.7, 24.25, 9.51],
            [10.0, 9.9, 9.8, 9.7, 24.25, 60.62],
            [10.0, 25.0, 62.5, 10.49, 10.38, 10.28]
        ]
        mg = PercentageMartingale(bet_results, user_input, inverted=True, multiplication_factor=2.5, round_limit=2)
        mg.simulate_strategy()
        #[print(bv) for bv in mg.bet_value_histories]
        self.assertEqual(mg.bet_value_histories, expected_bet_value_histories)
        # endregion


class TestFixedSoros(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """
        user_input['win_rate'] = 0.5000
        user_input['lose_rate'] = 0.5000
        user_input['payout_rate'] = 0.5000

        expected_bet_value_histories = [
            [10, 15.0, 22.5, 10, 15.0, 22.5],
            [10, 10, 10, 10, 10, 10],
            [10, 15.0, 10, 15.0, 10, 15.0],
            [10, 10, 15.0, 10, 15.0, 10],
            [10, 10, 10, 10, 15.0, 22.5],
            [10, 15.0, 22.5, 10, 10, 10]
        ]

        fs = FixedSoros(bet_results, user_input, rounds=2)
        fs.simulate_strategy()
        #[print(bv) for bv in fs.bet_value_histories]
        self.assertEqual(fs.bet_value_histories, expected_bet_value_histories)


class TestPercentageSoros(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """
        user_input['win_rate'] = 0.5000
        user_input['lose_rate'] = 0.5000
        user_input['payout_rate'] = 0.5000

        expected_bet_value_histories = [
            [10.0, 15.0, 22.5, 10.24, 15.36, 23.04],
            [10.0, 9.9, 9.8, 9.7, 9.61, 9.51],
            [10.0, 15.0, 9.9, 14.85, 9.8, 14.7],
            [10.0, 9.9, 14.85, 9.8, 14.7, 9.7],
            [10.0, 9.9, 9.8, 9.7, 14.55, 21.83],
            [10.0, 15.0, 22.5, 10.24, 10.14, 10.03]
        ]

        ps = PercentageSoros(bet_results, user_input, rounds=2)
        ps.simulate_strategy()
        #[print(bv) for bv in ps.bet_value_histories]
        self.assertEqual(ps.bet_value_histories, expected_bet_value_histories)


class TestFixedFibonacci(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """
        user_input['win_rate'] = 0.5000
        user_input['lose_rate'] = 0.5000
        user_input['payout_rate'] = 0.5000

        expected_bet_value_histories = [
            [10, 10, 10, 10, 10, 10],
            [10, 10, 20, 60, 300],
            [10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10],
            [10, 10, 20, 60, 10, 10],
            [10, 10, 10, 10, 10, 20]
        ]

        ff = FixedFibonacci(bet_results, user_input)
        ff.simulate_strategy()
        #[print(bv) for bv in ff.bet_value_histories]
        self.assertEqual(ff.bet_value_histories, expected_bet_value_histories)


class TestPercentageFibonacci(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """
        user_input['win_rate'] = 0.5000
        user_input['lose_rate'] = 0.5000
        user_input['payout_rate'] = 0.5000

        expected_bet_value_histories = [
            [10.0, 10.05, 10.1, 10.15, 10.2, 10.25],
            [10.0, 10.0, 20.0, 60.0, 300.0],
            [10.0, 10.05, 10.05, 10.0, 10.0, 9.95],
            [10.0, 10.0, 9.95, 9.95, 9.9, 9.9],
            [10.0, 10.0, 20.0, 60.0, 9.9, 9.95],
            [10.0, 10.05, 10.1, 10.15, 10.15, 20.3]
        ]

        pf = PercentageFibonacci(bet_results, user_input)
        pf.simulate_strategy()
        #[print(bv) for bv in pf.bet_value_histories]
        self.assertEqual(pf.bet_value_histories, expected_bet_value_histories)

'''
class TestFixedDAlembert(unittest.TestCase):
    def test_bet_value_histories(self):
        """
        Tests bet values histories ​​with predefined data
        """
        user_input['win_rate'] = 0.5000
        user_input['lose_rate'] = 0.5000
        user_input['payout_rate'] = 0.5000

        expected_bet_value_histories = [
            [10, 10, 10, 10, 10, 10],
            [10, 20, 30, 40, 50, 60],
            [50, 40, 50, 40, 50, 40],
            [30, 40, 30, 40, 30, 40],
            [30, 40, 50, 60, 50, 40],
            [30, 20, 10, 10, 20, 30]
        ]

        da = FixedDAlembert(bet_results, user_input)
        da.simulate_strategy()
        [print(bv) for bv in da.bet_value_histories]
        #self.assertEqual(da.bet_value_histories, expected_bet_value_histories)


if __name__ == '__main__':
    unittest.main()
