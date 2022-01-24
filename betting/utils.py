from scipy.constants import golden_ratio

def nth_fibonacci_number(n):
    return int(((golden_ratio**n) - (1 - golden_ratio)**n)/(5**(1/2)))

def get_bankroll_history_average(samples, bankroll_histories):
        bankroll_history_sum = []
        bankroll_history_average = []
        for i, bankroll_history in enumerate(bankroll_histories):
            for j, bankroll in enumerate(bankroll_history):
                if i == 0:
                    bankroll_history_sum.append(bankroll)
                else:
                    try:
                        bankroll_history_sum[j] += bankroll
                    except IndexError:
                        bankroll_history_sum.append(bankroll)

        for bankroll in bankroll_history_sum:
            bankroll_history_average.append(
                bankroll/samples)
        return bankroll_history_average

def get_bet_count_history(bankroll_history_average):
        try:
            bet_count_history = list(
                zip(*enumerate(bankroll_history_average, 1)))[0]
        except IndexError:
            return list()
        return bet_count_history
