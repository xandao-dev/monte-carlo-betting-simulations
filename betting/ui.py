'''
This code is a modification of 
https://github.com/HomelessSandwich/MonteCarloBettingSim

HomelessSandwich/MonteCarloBettingSim is licensed under MIT
'''

def print_stats(samples, bust_count, num_profitors, profits, loses, title):
    broke_percent = (bust_count / samples) * 100
    profit_percent = (num_profitors / samples) * 100
    try:
        survive_profit_percent = (num_profitors / (samples - bust_count)) * 100
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

    print(f'\n*{title.upper()}*\n')
    print(f'Percentage Broke: {broke_percent}%')
    print(f'Percentage Profited: {profit_percent}%')
    print(f'Percentage Survivors Profited: {survive_profit_percent}%')
    print(f'Average Profit: {avg_profit}')
    print(f'Average Loses: {avg_loses}')
    print(f'Expected Profit: {avg_profit * (profit_percent/ 100)}')
    print(f'Expected Loss: {avg_loses * (1 - (profit_percent / 100))}')
