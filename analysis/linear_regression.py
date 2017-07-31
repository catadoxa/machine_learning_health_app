#!/usr/bin/env python


from .data import Data
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import f_regression
import numpy as np
from pprint import pprint
from math import isnan

class LinearRegressionAnalysis:

    def __init__(self, data):
        self.X, self.Y, self.X_names = self.extract_data_to_arrays(data)
        self.set_regression()
        self.F_statistic, self.p_values = f_regression(self.X, self.Y)
        self.significance = [1 - (x if not isnan(x) else 1) for x in self.p_values]

    def extract_data_to_arrays(self, data):
        X = []
        Y = []
        X_names = [data.names[i] for i in range(len(data.names)) if not data.problems[i]]
        for value in data.data_dict.values():
            X_row = []
            Y_row = []
            for i in range(len(value)):
                if data.problems[i]:
                    Y_row.append(value[i])
                else:
                    X_row.append(value[i])
            X.append(X_row)
            Y.append(Y_row)
    #    pprint(Y)
    #    pprint(X)
    #    pprint(X_names)
        return np.array(X), np.array(Y), X_names   

    def set_regression(self):
        self.LR = LinearRegression(True, True, True)
        self.LR.fit(self.X, self.Y)
        self.R_squared = self.LR.score(self.X, self.Y)
    




