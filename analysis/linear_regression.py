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
        self.scores = self.calc_scores()
        self.low_day, self.low_margin, self.high_day, self.high_margin = self.average_days()

    def extract_data_to_arrays(self, data):
        X = []
        Y = []
        X_names = [data.names[i] for i in range(len(data.names)) if not data.problems[i]]
        for value in data.data_dict.values():
            X_row = []
            for i in range(len(value)):
                if data.problems[i]:
                    Y.append(value[i])
                else:
                    X_row.append(value[i])
            X.append(X_row)
        return np.array(X), np.array(Y), X_names   

    def set_regression(self):
        self.LR = LinearRegression(True, True, True)
        self.LR.fit(self.X, self.Y)
        self.R_squared = self.LR.score(self.X, self.Y)

    def calc_scores(self):
        #correlate each column of X against Y to find the score, multiply by 100 for clarity
        scores = []
        for i in range(len(self.X_names)):
            single_X = [[self.X[j][i]] for j in range(len(self.X))]
            reg = LinearRegression(True, True, True)
            reg.fit(single_X, self.Y)
            scores.append(100 * reg.score(single_X, self.Y))
        return scores

    def average_days(self):
        low = np.percentile(list(set(self.Y)), 25)
        high = np.percentile(list(set(self.Y)), 75)
        low_arry = high_arry = [0] * len(self.X_names)
        low_rows = high_rows = 0
        for row in self.X:
            y = self.LR.predict([row])
            if y <= low:
                low_arry = [low_arry[i] + row[i] for i in range(len(low_arry))]
                low_rows += 1
            if y >= high:
                high_arry = [high_arry[i] + row[i] for i in range(len(high_arry))]
                high_rows += 1
        return [el/low_rows for el in low_arry], low, [el/high_rows for el in high_arry], high



