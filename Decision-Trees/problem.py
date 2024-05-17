import numpy as np
import pandas as pd
import math
import os

class Problem:
    def __init__(self, file_path, target_attr, unnecessary_col=[]):
        self.df = self.load_csv(file_path, unnecessary_col)
        self.target_attr = target_attr
        self.entropy = self.calc_entropy()
        self.average_entropy = {}

    def load_csv(self, file_path, unnecessary_col):
        abs_path = os.path.abspath(file_path)
        df = pd.read_csv(abs_path)

        # Drop columns that they are unnecessary or have all values as NaN 
        nan_cols = df.isna().all()
        nan_cols = nan_cols[nan_cols].index.tolist()
        df.drop(columns=nan_cols + unnecessary_col, inplace=True)

        return df
    
    def calc_entropy(self):
        attributes = self.df.columns.tolist()
        attributes.remove(self.target_attr)
        entropy_dict = dict()

        for attr in attributes:
            values = self.df[attr].unique()
            entropy = dict()

            for val in values:
                counts = dict(self.df[self.df[attr] == val][self.target_attr].value_counts())
                total = sum(counts.values())
                H = -sum( (count/total) * math.log2(count/total) for count in counts.values())
                entropy[val] = H
            entropy_dict[attr] = entropy

        return entropy_dict
    
    def get_entropy_attribute(self, attribute):
        return self.entropy[attribute]
    
    # def get_average_entropy(self, attribute):

