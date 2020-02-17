import betting.strategies as strategies
from betting.statistical_calculations import *


class Stats():
    def __init__(
            self, bet_results=None, user_input=None, bankroll_histories=None,
            bet_value_histories=None, sl_reached_count=None, sg_reached_count=None,
            broke_count=None, profitors_count=None, profits=None, loses=None, title=None):
        self.bet_results = bet_results
        self.user_input = user_input
        self.bankroll_histories = bankroll_histories
        self.bet_value_histories = bet_value_histories
        self.sl_reached_count = sl_reached_count
        self.sg_reached_count = sg_reached_count
        self.broke_count = broke_count
        self.profitors_count = profitors_count
        self.profits = profits
        self.loses = loses
        self.title = title

    def print_indicators_tutorial(self, language=None):
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
            print(
                '''Percentage Survivors Who Profited (Percentual de Sobreviventes que Lucraram): \n''')
            print(
                '''Percentage Survivors Who NOT Profited (Percentual de Sobreviventes que NÃO Lucraram): \n''')
            print(
                '''ROI Percentage Average (Média do Retorno Sobre Investimento em porcentagem): \n''')
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
            print(
                '''ROI Percentage Average (Return On Investment Percentage Average): \n''')
            print('''Yield Percentage Average: \n''')
            print('''Final Bankroll Average: \n''')
            print('''Average Profit: \n''')
            print('''Average Loses: \n''')
            print('''Expected Profit: \n''')
            print('''Expected Loss: ''')
        print('-'*120)

    def __get_general_calculations(self):
        '''General Stats'''
        self.rate_of_return = calculate_expected_rate_of_return(
            self.user_input)
        # self.CDF_average = calculate_CDF_average_from_binomial_distribution(
        #    self.user_input, self.bet_results)

    def __get_strategy_calculations(self):
        # risk_of_ruin = calcule_risk_of_ruin(
        #    strategies.strategies_list[0], user_input)
        self.broke_percentage = calculate_broke_percentage(
            self.user_input, self.broke_count)
        self.profited_percentage = calculate_profited_percentage(
            self.user_input, self.profitors_count)
        self.survived_profited_percentage = calculate_survived_profited_percentage(
            self.user_input, self.broke_count, self.profitors_count)
        self.survived_NO_profited_percentage = calculate_survived_NO_profited_percentage(
            self.user_input, self.broke_count, self.profitors_count)
        self.ROI_percentage_average = calculate_ROI_percentage_average(
            self.user_input, self.bankroll_histories)
        self.yield_percentage_average = calculate_yield_percentage_average(
            self.user_input, self.bankroll_histories, self.bet_value_histories)
        self.average_of_number_of_bets = calculate_average_of_number_of_bets(
            self.user_input, self.bet_value_histories)
        self.final_bankroll_average = calculate_final_bankroll_average(
            self.user_input, self.bankroll_histories)
        self.average_profit = calculate_average_profit(self.profits)
        self.average_loses = calculate_average_loses(self.loses)
        self.expected_profit = calculate_expected_profit(
            self.average_profit, self.profited_percentage)
        self.expected_loss = calculate_expected_loss(
            self.average_loses, self.profited_percentage)

    def print_general_stats(self):
        self.__get_general_calculations()
        print('\n'+'-'*120)
        print('*GENERAL STATISTICS*')
        print(f'Expected Rate of Return: {self.rate_of_return}%')
        #print(f'CDF Average from Binomial Distribution: {self.CDF_average}%')
        print('-'*120)

    def print_strategy_stats(self, kelly_percentage=None) -> None:
        self.__get_strategy_calculations()
        print('\n'+'-'*120)
        print(f'*{self.title.upper()}*')

        if kelly_percentage is not None:
            print('Kelly criterion in percentage of capital: ' +
                  f'{round(kelly_percentage*100,2)}%\n')

        #print(f'Risk of Ruin: {risk_of_ruin}%')
        print(
            f'Percentage Broke: {self.broke_percentage}% ({self.broke_count} of {self.user_input["samples"]})')
        print(
            f'Percentage Profited: {self.profited_percentage}% ({self.profitors_count} of {self.user_input["samples"]})')
        print(
            f'Percentage Survivors Who Profited: {self.survived_profited_percentage}% ({self.profitors_count} of {self.user_input["samples"] - self.broke_count})')
        print(
            f'Percentage Survivors Who NOT Profited: {self.survived_NO_profited_percentage}% ({(self.user_input["samples"] - self.broke_count) - self.profitors_count} of {self.user_input["samples"] - self.broke_count})\n')

        print(f'ROI Percentage Average: {self.ROI_percentage_average}%')
        print(f'Yield Percentage Average: {self.yield_percentage_average}%\n')

        print(
            f'Final Bankroll Average: {self.user_input["currency"]} {self.final_bankroll_average}')
        print(
            f'Average Profit: {self.user_input["currency"]} {self.average_profit}')
        print(
            f'Average Loses: {self.user_input["currency"]} {self.average_loses}\n')

        print(
            f'Expected Profit: {self.user_input["currency"]} {self.expected_profit}')
        print(
            f'Expected Loss: {self.user_input["currency"]} {self.expected_loss}\n')

        print(
            f'Average of Number of Bets: {self.average_of_number_of_bets} bets')
        if self.user_input['stoploss'] is not None:
            print(
                f'{self.sl_reached_count} stoploss reached of {self.user_input["samples"]}')
        if self.user_input['stopgain'] is not None:
            print(
                f'{self.sg_reached_count} stopgain reached of {self.user_input["samples"]}')
        print('-'*120)
