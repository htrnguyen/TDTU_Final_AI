import pandas as pd
from problem import Problem

df = pd.read_csv("dt_data.csv")
p = Problem(df, "Rank", ["#"])

print(p.get_H_attribute("Q1"))
print(p.get_AE_attribute("Q1"))
print(p.get_IG_attribute("Q1"))
