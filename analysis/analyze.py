#!/usr/bin/env python

import json
from pprint import pprint
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import numpy as np
from flask import jsonify
from .data import Data
from .linear_regression import LinearRegressionAnalysis
import urllib


def analyze_kmeans(n, np_array):
    kmeans = KMeans(n_clusters=n)
    kmeans.fit(np_array)
    return kmeans


def analyze_linear_regression():
    pass



        

"""
turns the dict into a matrix, where each row contains the answers to the 
questions for a single date.
"""
def get_answers_to_matrix(data):
    arry = []
    for value in data.data_dict.values():
        arry.append(value)    
    return arry


def get_analysis(req_data):
    #get data
    #req_data = {"username": "123", "password": "123"}
    url = "http://web.engr.oregonstate.edu/~aluyorg/history.php"
    req_data = json.dumps(req_data).encode("utf8")
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    req = urllib.request.Request(url, req_data, headers)
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    data = Data(data)

#    #np_array = get_answers_to_matrix(data)
#    independent, target, independent_names = get_matrix_and_target(data)
#    lr = LinearRegression(True, True, True)
#    lr.fit(independent, target)
#    ret = []
#    print(lr.intercept_)
#    for i in range(len(independent_names)):
#        ret.append({independent_names[i]: str(lr.coef_[0][i])})
#    #pprint(np_array)
##    kmeans = analyze_kmeans(2, np_array)
##    centroids = kmeans.cluster_centers_
##    ret = []
##    for j in range(len(centroids)):
##        item = {}
##        for i in range(len(data.names)):
##            item[data.names[i]] = str(centroids[j][i])
##        ret.append(item)
##    #pprint(ret)
#    print("Mean: " + str(np.mean((target - lr.predict(independent))**2)))
#    for i in range(len(independent_names)):
#        col = [[independent[j][i]] for j in range(len(independent))]
#        print(col)
#        lrtwo = LinearRegression(True, True, True)
#        lrtwo.fit(col, target)
#        print("Mean " + independent_names[i] + ": " + str(np.mean((target - lrtwo.predict(col))**2)))
#this is the good stuff
    ret = []
    LRA = LinearRegressionAnalysis(data)
    for i in range(len(LRA.X_names)):
        ret.append({LRA.X_names[i] + " coefficient": str(LRA.LR.coef_[0][i])})
        ret.append({LRA.X_names[i] + " p value": str(LRA.p_values[i])})
        ret.append({LRA.X_names[i] + " F statistic": str(LRA.F_statistic[i])})
        ret.append({LRA.X_names[i] + " significance": str(LRA.significance[i])})
    ret.append({"R squared": str(LRA.R_squared)})
    ret.append({"intercept": str(LRA.LR.intercept_)})
    return jsonify(ret)



