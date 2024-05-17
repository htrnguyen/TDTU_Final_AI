from problem import Problem
import pandas as pd

df = pd.read_csv('./dt_data.csv')
p = Problem(df, 'Rank', ['#'])

print(p.get_H_attribute('Q2'))
print(p.get_AE_attribute('Q2'))
print(p.get_IG_attribute('Q2'))
