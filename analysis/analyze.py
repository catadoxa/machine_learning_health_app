#!/usr/bin/env python

from flask import jsonify
from .data import Data
from .linear_regression import LinearRegressionAnalysis
from .kmeans_clustering import KMeansClusteringAnalysis
import urllib


def get_analysis(req_data):
    #data = Data(data)
    data = Data(req_data)
    ret = {}
    ret["feature-data"] = []
    LRA = LinearRegressionAnalysis(data)
    kmeans = KMeansClusteringAnalysis(data)
    ret["average-high"] = {}
    ret["average-low"] = {}
    ret["average-high"][data.problem + "-greater-than"] = "{0:.2f}".format(LRA.high_margin)
    ret["average-low"][data.problem + "-less-than"] = "{0:.2f}".format(LRA.low_margin)
    ret["average-day"] = {}
    ret["clusters"] = kmeans.return_data
    for i in range(len(LRA.X_names)):
        obj = {}
        obj['problem'] = data.problem
        obj['input'] = LRA.X_names[i]
        obj['significance'] = "{0:.2f}".format(LRA.scores[i])
        obj['coefficient'] = "{0:.2f}".format(LRA.LR.coef_[i])
        ret["feature-data"].append(obj)
        ret["average-high"][LRA.X_names[i]] = "{0:.2f}".format(LRA.high_day[i])
        ret["average-low"][LRA.X_names[i]] = "{0:.2f}".format(LRA.low_day[i])
    for i in range(len(data.names)):
        ret["average-day"][data.names[i]] = "{0:.2f}".format(data.averages[i])
    error = False
    if(len(data.data) < 5):
        error = True
    ret["error"] = error
    return jsonify(ret)



