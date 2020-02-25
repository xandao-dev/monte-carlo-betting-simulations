import betting.Strategies as strategies
from scipy.stats import binom


def calculate_expected_rate_of_return(user_input):
    '''
    The expected return is the profit or loss an investor anticipates on an
    investment that has known or anticipated rates of return (RoR). It is
    calculated by multiplying potential outcomes by the chances of them
    occurring and then totaling these results.
    For example, if an investment has a 55% chance of gaining 87% and a 45%
    chance of losing 100%, the expected return is 2.85%
    (55% x 87% + 45% x -100% = 2.85%).

    A 'ror' of 3% means that you tend to win 3% of your stake in the long run.
    '''
    rate_of_return = round((user_input['win_rate']*user_input['payout_rate'] -
                            user_input['lose_rate']*1)*100, 2)
    # *1 because you lose your entire bet
    return rate_of_return


def calculate_cdf_average_from_binomial_distribution(user_input, bet_results):
    cdf_sum = 0
    for sample_result in bet_results:
        true_results = sum(1 for x in sample_result if x == True)
        cdf_sum += binom.cdf(true_results,
                             user_input['bet_count'], user_input['win_rate'])
    cdf_average = round((cdf_sum/user_input['samples'])*100, 2)
    return cdf_average


# FIXME: I think this formula is wrong because of payout.
def calcule_risk_of_ruin(current_strategy, user_input):
    '''
    Risk of ruin is a concept in gambling, insurance, and finance relating to
    the likelihood of losing all one's investment capital[1] or extinguishing
    one's bankroll below the minimum for further play. For instance, if someone
    bets all their money on a simple coin toss, the risk of ruin is 50%. In a
    multiple-bet scenario, risk of ruin accumulates with the number of bets:
    each repeated play increases the risk, and persistent play ultimately
    yields the stochastic certainty of gambler's ruin.

    Formula: Risk of Ruin = ((1 - (W*R - L)) / (1 + (W*R - L)))^U
        Where:
            W = the probability of a desirable outcome, or a win
            L = the probability of an undesirable outcome, or a loss
            R = Payout Rate, 0 <= R <= 1
            U = the maximum number of risks that can be taken before the
                individual reaches their threshold for ruin
    '''

    units = 0
    if current_strategy == strategies.strategies_list[0]:
        try:
            units = (user_input['initial_bankroll'] -
                     user_input['stoploss'])/user_input['bet_value']
        except TypeError:
            units = user_input['initial_bankroll']/user_input['bet_value']

    risk_of_ruin = (
        (1 - (user_input['win_rate']*user_input['payout_rate'] - user_input['lose_rate'])) /
        (1 + (user_input['win_rate']*user_input['payout_rate'] - user_input['lose_rate'])))**units
    return round(risk_of_ruin*100, 2)


def calculate_broke_percentage(user_input, broke_count):
    return round((broke_count / user_input['samples']) * 100, 2)


def calculate_profited_percentage(user_input, profitors_count):
    return round((profitors_count / user_input['samples']) * 100, 2)


def calculate_survived_profited_percentage(user_input, broke_count, profitors_count):
    try:
        survive_profit_percent = round(
            (profitors_count / (user_input['samples'] - broke_count)) * 100, 2)
    except ZeroDivisionError:
        survive_profit_percent = 0
    return survive_profit_percent


def calculate_survived_no_profited_percentage(user_input, broke_count, profitors_count):
    try:
        survive_NO_profit_percent = round(
            ((((user_input['samples'] - broke_count)) - profitors_count) /
                (user_input['samples'] - broke_count)) * 100, 2)
    except ZeroDivisionError:
        survive_NO_profit_percent = 0
    return survive_NO_profit_percent


def calculate_roi_percentage_average(user_input, bankroll_histories):
    roi_sum = 0
    for bankroll_history in bankroll_histories:
        roi_sum += ((bankroll_history[-1] - user_input['initial_bankroll']) / user_input['initial_bankroll'])*100
    roi_percentage_average = round(roi_sum/user_input['samples'], 2)
    return roi_percentage_average


def calculate_yield_percentage_average(user_input, bankroll_histories, bet_value_histories):
    bet_value_sum = 0
    yield_sum = 0
    for bankroll_history, bet_value_history in zip(bankroll_histories, bet_value_histories):
        bet_value_sum = sum(bet_value_history)
        yield_sum += ((bankroll_history[-1] - user_input['initial_bankroll'])/bet_value_sum)*100

    yield_percentage_average = round(yield_sum/user_input['samples'], 2)
    return yield_percentage_average


def calculate_average_of_number_of_bets(user_input, bet_value_histories):
    number_of_bets = 0
    for bet_value_history in bet_value_histories:
        number_of_bets += len(bet_value_history)
    average_of_number_of_bets = int(number_of_bets/user_input['samples'])
    return average_of_number_of_bets


def calculate_final_bankroll_average(user_input, bankroll_histories):
    final_bankroll_sum = 0
    for bankroll_history in bankroll_histories: final_bankroll_sum += bankroll_history[-1]
    final_bankroll_average = round(final_bankroll_sum/user_input['samples'], 2)
    return final_bankroll_average


def calculate_average_profit(profits):
    try:
        average_profit = round(sum(profits) / len(profits), 2)
    except ZeroDivisionError:
        average_profit = 0
    return average_profit


def calculate_average_loses(loses):
    try:
        average_loses = round(sum(loses) / len(loses), 2)
    except ZeroDivisionError:
        average_loses = 0
    return average_loses


def calculate_expected_profit(average_profit, profited_percentage):
    return round(average_profit * (profited_percentage / 100), 2)


def calculate_expected_loss(average_loses, profited_percentage):
    return round(average_loses * (1 - (profited_percentage / 100)), 2)
