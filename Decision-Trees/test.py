from problem import Problem

p = Problem('dt_data.csv', 'Rank', ['#'])

print(p.get_H_attribute('Q2'))
print(p.get_AE_attribute('Q2'))
print(p.get_IG_attribute('Q2'))
