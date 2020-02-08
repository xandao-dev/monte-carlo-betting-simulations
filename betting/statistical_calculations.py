from betting.strategies import strategies


def calcule_risk_of_ruin(current_strategy, user_input):
    '''
    Risk of ruin is a concept in gambling, insurance, and finance relating to 
    the likelihood of losing all one's investment capital[1] or extinguishing 
    one's bankroll below the minimum for further play. For instance, if someone 
    bets all their money on a simple coin toss, the risk of ruin is 50%. In a 
    multiple-bet scenario, risk of ruin accumulates with the number of bets: 
    each repeated play increases the risk, and persistent play ultimately 
    yields the stochastic certainty of gambler's ruin.

    Formula: risk_of_ruin = ((1 – Edge)/(1 + Edge)) ^ Capital_Units
        or
    Formula: Risk of Ruin = ((1 - (W - L)) / (1 + (W - L)))^U
        Where:
            W = the probability of a desirable outcome, or a win
            L = the probability of an undesirable outcome, or a loss
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
        (1 - (user_input['win_rate'] - user_input['lose_rate'])) /
        (1 + (user_input['win_rate'] - user_input['lose_rate']))) ** units

    return round(risk_of_ruin, 2)
