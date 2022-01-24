
from typing import List
from random import uniform


class BetGenerator:
    def __init__(self, user_input):
        self.user_input = user_input

    def generate_random_bet_results(self) -> List[List[bool]]:
        bet_results = []
        for _ in range(self.user_input['samples']):
            results_temp = []
            for _ in range(self.user_input['bet_count']):
                result = round(uniform(0, 1), 4)
                if result <= self.user_input['win_rate']:
                    results_temp.append(True)
                elif result > self.user_input['win_rate']:
                    results_temp.append(False)
            bet_results.append(results_temp.copy())
        return bet_results