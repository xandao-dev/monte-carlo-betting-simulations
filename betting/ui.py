'''
This code is a modification of 
https://github.com/HomelessSandwich/MonteCarloBettingSim

HomelessSandwich/MonteCarloBettingSim is licensed under MIT
'''

from betting.statistical_calculations import *
import betting.strategies as strategies


def print_indicators_tutorial(language=None):
    print('\n'+'-'*80)
    if language == 'PORTUGUESE':
        print('''Expected Rate of Return (Taxa de Retorno Esperada):  Um RoR de 3% significa 
    que você tende a ganhar 3% do valor da sua aposta no longo prazo.\n''')
        print('''CDF Average from Binomial Distribution (Média CDF da Distribuição Binomial): ''')
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
        print('''CDF Average from Binomial Distribution: ''')
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


def print_general_stats(bet_results, user_input):
    print('\n'+'-'*80)
    print('*GENERAL STATISTICS*')
    rate_of_return = calculate_expected_rate_of_return(user_input)
    CDF_average = calculate_CDF_average_from_binomial_distribution(
        user_input, bet_results)
    print(f'Expected Rate of Return: {rate_of_return}%')
    print(f'CDF Average from Binomial Distribution: {CDF_average}%')
    print('-'*80)


def print_strategy_stats(
    user_input, bankroll_histories, broke_count, profitors_count,
    profits, loses, title, kelly_percentage=None
) -> None:
    risk_of_ruin = calcule_risk_of_ruin(
        strategies.strategies_list[0], user_input)
    broke_percentage = calculate_broke_percentage(user_input, broke_count)
    profited_percentage = calculate_profited_percentage(
        user_input, profitors_count)
    survived_profited_percentage = calculate_survived_profited_percentage(
        user_input, broke_count, profitors_count)
    final_bankroll_average = calculate_final_bankroll_average(
        user_input, bankroll_histories)
    average_profit = calculate_average_profit(profits)
    average_loses = calculate_average_loses(loses)
    expected_profit = calculate_expected_profit(
        average_profit, profited_percentage)
    expected_loss = calculate_expected_loss(average_loses, profited_percentage)

    print('\n'+'-'*80)
    print(f'*{title.upper()}*')

    if kelly_percentage is not None:
        print('Kelly criterion in percentage of capital: ' +
              f'{round(kelly_percentage*100,2)}%\n')

    #print(f'Risk of Ruin: {risk_of_ruin}%')
    print(f'Percentage Broke: {broke_percentage}%')
    print(f'Percentage Profited: {profited_percentage}%')
    print(f'Percentage Survivors Profited: {survived_profited_percentage}%\n')

    print(
        f'Final Bankroll Average: {user_input["currency"]} {final_bankroll_average}')
    print(f'Average Profit: {user_input["currency"]} {average_profit}')
    print(f'Average Loses: {user_input["currency"]} {average_loses}\n')

    print(f'Expected Profit: {user_input["currency"]} {expected_profit}')
    print(f'Expected Loss: {user_input["currency"]} {expected_loss}')
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
