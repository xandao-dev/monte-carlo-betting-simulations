'''
This code is a modification of 
https://github.com/HomelessSandwich/MonteCarloBettingSim

HomelessSandwich/MonteCarloBettingSim is licensed under MIT
'''


def print_stats(
    user_input, bankroll_histories, broke_count, profitors_count,
    profits, loses, title, kelly_percentage=None
) -> None:

    broke_percent = (broke_count / user_input['samples']) * 100
    profit_percent = (profitors_count / user_input['samples']) * 100

    final_bankroll_sum = 0
    for bankroll_history in bankroll_histories:
        final_bankroll_sum += bankroll_history[-1]
    final_bankroll_average = final_bankroll_sum/user_input['samples']

    try:
        survive_profit_percent = (
            profitors_count / (user_input['samples'] - broke_count)) * 100
    except ZeroDivisionError:
        survive_profit_percent = 0
    try:
        avg_profit = sum(profits) / len(profits)
    except ZeroDivisionError:
        avg_profit = 0
    try:
        avg_loses = sum(loses) / len(loses)
    except ZeroDivisionError:
        avg_loses = 0

    print(f'\n*{title.upper()}*')
    if kelly_percentage is not None:
        print('Kelly criterion in percentage of capital: ' +
              f'{round(kelly_percentage*100,2)}%')
    print(f'Percentage Broke: {broke_percent}%')
    print(f'Percentage Profited: {profit_percent}%')
    print(f'Percentage Survivors Profited: {survive_profit_percent}%')
    print(f'Final Bankroll Average: {final_bankroll_average}')
    print(f'Average Profit: {avg_profit}')
    print(f'Average Loses: {avg_loses}')
    print(f'Expected Profit: {avg_profit * (profit_percent/ 100)}')
    print(f'Expected Loss: {avg_loses * (1 - (profit_percent / 100))}')


'''
    print(f'Final bankroll average: {round(bankroll_average,2)}')
    print(f'Death rate: {round((bust_count/samples)*100,2)}%, '
          f'Survival rate: {100.0 - round((bust_count/samples)*100,2)}%')
    print(f'{bust_count} broken of {samples} samples in Fixed Sys.!')
    print(f'{sl_reached_count} stoploss reached of {samples} in Fixed Sys.!')
    print(f'{sg_reached_count} stopgain reached of {samples} in Fixed Sys.!\n')
'''
