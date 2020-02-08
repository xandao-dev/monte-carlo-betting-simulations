def calcule_risk_of_ruin():
    '''
    Risk of ruin is a concept in gambling, insurance, and finance relating to 
    the likelihood of losing all one's investment capital[1] or extinguishing 
    one's bankroll below the minimum for further play. For instance, if someone 
    bets all their money on a simple coin toss, the risk of ruin is 50%. In a 
    multiple-bet scenario, risk of ruin accumulates with the number of bets: 
    each repeated play increases the risk, and persistent play ultimately 
    yields the stochastic certainty of gambler's ruin.

    Formula: risk_of_ruin = ((1 – Edge)/(1 + Edge)) ^ Capital_Units
    ''' 
    