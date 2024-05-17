import numpy as np
import pandas as pd
import math
import os

class Problem:
    def __init__(self, dataframe, target_attribute, unnecessary_col=[]):
        self.df = self.set_df(dataframe, unnecessary_col)
        self.target_attr = target_attribute
        self.attributes = self.set_attribute()
        self.H, self.AE, self.IG = self.calc_H_A_IG()

    def set_df(self, dataframe, unnecessary_col):
        # Drop columns that they are unnecessary or have all values as NaN 
        df = dataframe.copy()
        nan_cols = df.isna().all()
        nan_cols = nan_cols[nan_cols].index.tolist()
        df.drop(columns=nan_cols + unnecessary_col, inplace=True)

        return df
    
    def set_attribute(self):
        attributes = self.df.columns.tolist()
        attributes.remove(self.target_attr)
        return attributes
    
    def calc_H_A_IG(self):
        entropies = dict()
        average_entropies = dict()
        information_gains = dict()
        H_target = 0
        target_values = self.df[self.target_attr].unique()
        total = len(self.df[self.target_attr])

        # Calculate entropy of target attribute
        for t_var in target_values:
            counts = self.df[self.df[self.target_attr] == t_var][self.target_attr].value_counts().to_dict()
            
            for count in counts.values():
                H_target += -(count/total) * math.log2(count/total)

        # Calculate entropy, average entropy and information gain of other attributes
        for attr in self.attributes:
            values = self.df[attr].unique() # value of attribute (Ex: 'Q1' have 8 values: 0,1,2,3,4,5,6,7)
            entropy = dict()
            I = 0

            for val in values:
                counts = self.df[self.df[attr] == val][self.target_attr].value_counts().to_dict()
                total = sum(counts.values())
                H = 0

                for count in counts.values():
                    H += -(count/total) * math.log2(count/total)

                entropy[val] = H
                I += total / len(self.df[attr]) * H
                
            entropies[attr] = entropy
            average_entropies[attr] = I
            information_gains[attr] = H_target - average_entropies[attr]
        
        return entropies, average_entropies, information_gains

    def get_H_attribute(self, attribute):
        return self.H[attribute]
    
    def get_AE_attribute(self, attribute):
        return self.AE[attribute]
    
    def get_IG_attribute(self, attribute):
        return self.IG[attribute]
    
    

