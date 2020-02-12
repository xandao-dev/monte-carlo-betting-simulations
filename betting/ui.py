'''
This code is a modification of 
https://github.com/HomelessSandwich/MonteCarloBettingSim

HomelessSandwich/MonteCarloBettingSim is licensed under MIT
'''

from betting.statistical_calculations import *
import betting.strategies as strategies


def print_indicators_tutorial(language=None):
    print('\n'+'-'*120)
    if language == 'PORTUGUESE':
        print('''Expected Rate of Return (Taxa de Retorno Esperada):  Um RoR de 3% significa 
    que você tende a ganhar 3% do valor da sua aposta no longo prazo.\n''')
        #print('''CDF Average from Binomial Distribution (Média CDF da Distribuição Binomial): ''')
        print('''Kelly criterion in percentage of capital (Critério de Kelly em
    porcentagem de capital): \n''')
        #print('''Risk of Ruin(Risco de Ruína): \n''')
        print('''Percentage Broke (Percentual de Quebra): \n''')
        print('''Percentage Profited (Percentual de Lucro): \n''')
        print('''Percentage Survivors Who Profited (Percentual de Sobreviventes que Lucraram): \n''')
        print('''Percentage Survivors Who NOT Profited (Percentual de Sobreviventes que NÃO Lucraram): \n''')
        print('''ROI Percentage Average (Média do Retorno Sobre Investimento em porcentagem): \n''')
        print('''Yield Percentage Average (Porcentagem Média Média): \n''')
        print('''Final Bankroll Average (Média Final da Banca): \n''')
        print('''Average Profit (Média dos Lucros): \n''')
        print('''Average Loses (Média das Perdas): \n''')
        print('''Expected Profit (Lucro Esperado): \n''')
        print('''Expected Loss (Perda Esperada): ''')
    else:
        print('''Expected Rate of Return:  A RoR of 3% means that you tend to win 3% of your 
    stake in the long run.\n''')
        #print('''CDF Average from Binomial Distribution: ''')
        print('''Kelly criterion in percentage of capital: \n''')
        #print('''Risk of Ruin: \n''')
        print('''Percentage Broke: \n''')
        print('''Percentage Profited: \n''')
        print('''Percentage Survivors Who Profited: \n''')
        print('''Percentage Survivors Who NOT Profited: \n''')
        print('''ROI Percentage Average (Return On Investment Percentage Average): \n''')
        print('''Yield Percentage Average: \n''')
        print('''Final Bankroll Average: \n''')
        print('''Average Profit: \n''')
        print('''Average Loses: \n''')
        print('''Expected Profit: \n''')
        print('''Expected Loss: ''')
    print('-'*120)


def print_general_stats(bet_results, user_input):
    print('\n'+'-'*120)
    print('*GENERAL STATISTICS*')
    rate_of_return = calculate_expected_rate_of_return(user_input)
    CDF_average = calculate_CDF_average_from_binomial_distribution(
        user_input, bet_results)
    print(f'Expected Rate of Return: {rate_of_return}%')
    #print(f'CDF Average from Binomial Distribution: {CDF_average}%')
    print('-'*120)


def print_strategy_stats(
    user_input, bankroll_histories, bet_value_histories, broke_count,
    sl_reached_count, sg_reached_count, profitors_count, profits, loses, title, 
    kelly_percentage=None
) -> None:
    risk_of_ruin = calcule_risk_of_ruin(
        strategies.strategies_list[0], user_input)
    broke_percentage = calculate_broke_percentage(user_input, broke_count)
    profited_percentage = calculate_profited_percentage(
        user_input, profitors_count)
    survived_profited_percentage = calculate_survived_profited_percentage(
        user_input, broke_count, profitors_count)
    survived_NO_profited_percentage = calculate_survived_NO_profited_percentage(
        user_input, broke_count, profitors_count)
    ROI_percentage_average = calculate_ROI_percentage_average(
        user_input, bankroll_histories)
    yield_percentage_average = calculate_yield_percentage_average(
        user_input, bankroll_histories, bet_value_histories)
    average_of_number_of_bets = calculate_average_of_number_of_bets(
        user_input, bet_value_histories)
    final_bankroll_average = calculate_final_bankroll_average(
        user_input, bankroll_histories)
    average_profit = calculate_average_profit(profits)
    average_loses = calculate_average_loses(loses)
    expected_profit = calculate_expected_profit(
        average_profit, profited_percentage)
    expected_loss = calculate_expected_loss(average_loses, profited_percentage)

    print('\n'+'-'*120)
    print(f'*{title.upper()}*')

    if kelly_percentage is not None:
        print('Kelly criterion in percentage of capital: ' +
              f'{round(kelly_percentage*100,2)}%\n')

    #print(f'Risk of Ruin: {risk_of_ruin}%')
    print(
        f'Percentage Broke: {broke_percentage}% ({broke_count} of {user_input["samples"]})')
    print(
        f'Percentage Profited: {profited_percentage}% ({profitors_count} of {user_input["samples"]})')
    print(
        f'Percentage Survivors Who Profited: {survived_profited_percentage}% ({profitors_count} of {user_input["samples"] - broke_count})')
    print(
        f'Percentage Survivors Who NOT Profited: {survived_NO_profited_percentage}% ({(user_input["samples"] - broke_count) - profitors_count} of {user_input["samples"] - broke_count})\n')

    print(f'ROI Percentage Average: {ROI_percentage_average}%')
    print(f'Yield Percentage Average: {yield_percentage_average}%\n')

    print(
        f'Final Bankroll Average: {user_input["currency"]} {final_bankroll_average}')
    print(f'Average Profit: {user_input["currency"]} {average_profit}')
    print(f'Average Loses: {user_input["currency"]} {average_loses}\n')

    print(f'Expected Profit: {user_input["currency"]} {expected_profit}')
    print(f'Expected Loss: {user_input["currency"]} {expected_loss}\n')

    print(f'Average of Number of Bets: {average_of_number_of_bets} bets')
    if user_input['stoploss'] is not None:
        print(f'{sl_reached_count} stoploss reached of {user_input["samples"]}')
    if user_input['stopgain'] is not None:
        print(f'{sg_reached_count} stopgain reached of {user_input["samples"]}')
    print('-'*120)
