from problem import Problem

p = Problem('dt_data.csv', 'Rank', ['#'])

print(p.get_entropy_attribute('Q1'))