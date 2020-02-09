'''
This code is a modification of 
https://github.com/HomelessSandwich/MonteCarloBettingSim

HomelessSandwich/MonteCarloBettingSim is licensed under MIT
'''

from betting.statistical_calculations import *


def print_indicators_tutorial(language=None):
    print('\n'+'-'*80)
    if language == 'PORTUGUESE':
        print('''Expected Rate of Return (Taxa de Retorno Esperada):  Um RoR de 3% significa 
    que você tende a ganhar 3% do valor da sua aposta no longo prazo.\n''')
        print('''Kelly criterion in percentage of capital (Critério de Kelly em
    porcentagem de capital): \n''')
        #print('''Risk of Ruin(Risco de Ruína): \n''')
        print('''Percentage Broke (Percentual de Quebra): \n''')
        print('''Percentage Profited (Percentual de Lucro): \n''')
        print('''Percentage Survivors Profited (Percentual de Sobreviventes que Lucraram): \n''')
        print('''Final Bankroll Average (Média Final da Banca): \n''')
        print('''Average Profit (Média dos Lucros): \n''')
        print('''Average Loses (Média das Perdas): \n''')
        print('''Expected Profit (Lucro Esperado): \n''')
        print('''Expected Loss (Perda Esperada): ''')
    else:
        print('''Expected Rate of Return:  A RoR of 3% means that you tend to win 3% of your 
    stake in the long run.\n''')
        print('''Kelly criterion in percentage of capital: \n''')
        #print('''Risk of Ruin: \n''')
        print('''Percentage Broke: \n''')
        print('''Percentage Profited: \n''')
        print('''Percentage Survivors Profited: \n''')
        print('''Final Bankroll Average: \n''')
        print('''Average Profit: \n''')
        print('''Average Loses: \n''')
        print('''Expected Profit: \n''')
        print('''Expected Loss: ''')
    print('-'*80)


def print_general_stats(user_input):
    print('\n'+'-'*80)
    print('*GENERAL STATISTICS*')
    rate_of_return = calculate_expected_rate_of_return(user_input)
    print(f'Expected Rate of Return: {rate_of_return}%')
    print('-'*80)


def print_strategy_stats(
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

    risk_of_ruin = calcule_risk_of_ruin(strategies[0], user_input)

    print('\n'+'-'*80)
    print(f'*{title.upper()}*')
    if kelly_percentage is not None:
        print('Kelly criterion in percentage of capital: ' +
              f'{round(kelly_percentage*100,2)}%\n')
    #print(f'Risk of Ruin: {risk_of_ruin}%')
    print(f'Percentage Broke: {broke_percent}%')
    print(f'Percentage Profited: {profit_percent}%')
    print(f'Percentage Survivors Profited: {survive_profit_percent}%\n')
    print(
        f'Final Bankroll Average: {user_input["currency"]} {final_bankroll_average}')
    print(f'Average Profit: {user_input["currency"]} {avg_profit}')
    print(f'Average Loses: {user_input["currency"]} {avg_loses}\n')
    print(
        f'Expected Profit: {user_input["currency"]} {round(avg_profit * (profit_percent/ 100), 2)}')
    print(
        f'Expected Loss: {user_input["currency"]} {round(avg_loses * (1 - (profit_percent / 100)), 2)}\n')
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
