strategies = ['fixed_bettor', 'percentage_bettor', 'kelly_criterion',
              'fixed_martingale', 'percentage_martingale']


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
    rate_of_return = user_input['win_rate']*user_input['payout_rate'] - \
        user_input['lose_rate']*1
    return rate_of_return


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
    if current_strategy == strategies[0]:
        if user_input['stoploss'] is None:
            user_input['stoploss'] = 0
        units = (user_input['initial_bankroll'] -
                 user_input['stoploss'])/user_input['bet_value']

    risk_of_ruin = (
        (1 - (user_input['win_rate']*user_input['payout_rate'] - user_input['lose_rate'])) /
        (1 + (user_input['win_rate']*user_input['payout_rate'] - user_input['lose_rate'])))**units
    return round(risk_of_ruin*100, 2)
