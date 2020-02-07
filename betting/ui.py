'''
This code is a modification of 
https://github.com/HomelessSandwich/MonteCarloBettingSim

HomelessSandwich/MonteCarloBettingSim is licensed under MIT
'''


def print_stats(
    user_input, bankroll_histories, broke_count, profitors_count,
    profits, loses, title, kelly_percentage=None
) -> None:

    broke_percent = round((broke_count / user_input['samples']) * 100, 2)
    profit_percent = round((profitors_count / user_input['samples']) * 100, 2)

    final_bankroll_sum = 0
    for bankroll_history in bankroll_histories:
        final_bankroll_sum += bankroll_history[-1]
    final_bankroll_average = round(final_bankroll_sum/user_input['samples'], 2)

    try:
        survive_profit_percent = round(
            (profitors_count / (user_input['samples'] - broke_count)) * 100, 2)
    except ZeroDivisionError:
        survive_profit_percent = 0
    try:
        avg_profit = round(sum(profits) / len(profits), 2)
    except ZeroDivisionError:
        avg_profit = 0
    try:
        avg_loses = round(sum(loses) / len(loses), 2)
    except ZeroDivisionError:
        avg_loses = 0
    print('\n'+'-'*80)
    print(user_input['currency'])
    print(f'*{title.upper()}*')
    if kelly_percentage is not None:
        print('Kelly criterion in percentage of capital: ' +
              f'{round(kelly_percentage*100,2)}%')
    print(f'Percentage Broke: {broke_percent}%')
    print(f'Percentage Profited: {profit_percent}%')
    print(f'Percentage Survivors Profited: {survive_profit_percent}%')
    print(
        f'Final Bankroll Average: {user_input["currency"]} {final_bankroll_average}')
    print(f'Average Profit: {user_input["currency"]} {avg_profit}')
    print(f'Average Loses: {user_input["currency"]} {avg_loses}')
    print(
        f'Expected Profit: {user_input["currency"]} {round(avg_profit * (profit_percent/ 100), 2)}')
    print(
        f'Expected Loss: {user_input["currency"]} {round(avg_loses * (1 - (profit_percent / 100)), 2)}')
    print('-'*80)


'''
    print 'number_of_player_win: %s, Percentage: %f %%' % (str(number_of_player_win), float(number_of_player_win/number_of_hand)*100)
    print 'number_of_banker_win: %s, Percentage: %f %%' % (str(number_of_banker_win), float(number_of_banker_win/number_of_hand)*100)
    print 'number_of_tie: %s, Percentage: %f %%' % (str(number_of_tie), float(number_of_tie/number_of_hand)*100)
    print 'number_of_hand: %s' % str(number_of_hand)
    print 'bet: %s' % str(bet)
    print 'start_bankroll: %s' % str(start_bankroll)
    print 'final_bankroll: %s' % str(bankroll)
    print 'number_of_bet: %s' % str(number_of_bet)
    print 'Total_bet_value： %s' % str(number_of_bet*bet)
    print 'House edge： %s' % str(number_of_bet*bet*0.0106)
    print 'Real Loss： %s' % str(float(start_bankroll-bankroll))
    print 'i_bet_number_of_banker_win: %s' % str(i_bet_number_of_banker_win) 
    print 'i_bet_number_of_player_win: %s' % str(i_bet_number_of_player_win) 
    print 'number_of_win: %s' % str(number_of_win)
    print 'number_of_push: %s' % str(number_of_push) 
    print 'number_of_total_loss: %s' % str(number_of_total_loss)
'''


'''
    print(f'Final bankroll average: {round(bankroll_average,2)}')
    print(f'Death rate: {round((bust_count/samples)*100,2)}%, '
          f'Survival rate: {100.0 - round((bust_count/samples)*100,2)}%')
    print(f'{bust_count} broken of {samples} samples in Fixed Sys.!')
    print(f'{sl_reached_count} stoploss reached of {samples} in Fixed Sys.!')
    print(f'{sg_reached_count} stopgain reached of {samples} in Fixed Sys.!\n')
'''
