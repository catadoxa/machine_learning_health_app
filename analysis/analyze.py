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


# """
# turns the dict into a matrix, where each row contains the answers to the
# questions for a single date.
# """
# def get_answers_to_matrix(data):
#     arry = []
#     for value in data.data_dict.values():
#         arry.append(value)
#     return arry


def get_analysis(req_data):
    # url = "http://web.engr.oregonstate.edu/~aluyorg/history.php"
    # req_data = json.dumps(req_data).encode("utf8")
    # headers = {"Content-type": "application/json", "Accept": "text/plain"}
    # req = urllib.request.Request(url, req_data, headers)
    # resp = urllib.request.urlopen(req)
    # data = json.loads(resp.read())
    # data = Data(data)

    data = Data(req_data)
    ret = {}
    ret["feature-data"] = []
    LRA = LinearRegressionAnalysis(data)

    ret["average-high"] = {}
    ret["average-low"] = {}
    ret["average-high"][data.problem + "-greater-than"] = "{0:.2f}".format(LRA.high_margin)
    ret["average-low"][data.problem + "-less-than"] = "{0:.2f}".format(LRA.low_margin)
    ret["average-day"] = {}
    ret["clusters"] = []
    for i in range(len(LRA.X_names)):
        obj = {}
        obj['problem'] = data.problem
        obj['input'] = LRA.X_names[i]
        obj['significance'] = "{0:.2f}".format(LRA.scores[i])
        obj['coefficient'] = "{0:.2f}".format(LRA.LR.coef_[i])
        ret["feature-data"].append(obj)
        ret["average-high"][LRA.X_names[i]] = "{0:.2f}".format(LRA.high_day[i])
        ret["average-low"][LRA.X_names[i]] = "{0:.2f}".format(LRA.low_day[i])
        ret["average-day"][data.names[i]] = "{0:.2f}".format(data.averages[i])
    return jsonify(ret)



