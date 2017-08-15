#!/usr/bin/env python

from flask import jsonify
from .data import Data
from .linear_regression import LinearRegressionAnalysis
from .kmeans_clustering import KMeansClusteringAnalysis
import urllib


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
        ret["average-day"][data.names[i]] = "{0:.2f}".format(data.averages[i])
    return jsonify(ret)



