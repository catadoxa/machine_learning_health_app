#!/usr/bin/env python

import json
from pprint import pprint
from sklearn.cluster import KMeans
import numpy
from flask import jsonify


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def to_array_dict(data):
    data = dict(data)
    data_dict = {}
    headers = []
    for key, value in data.items():
        data_dict[key] = []        
        vals = list(value)
        for val in vals:
            question = dict(val)
            if not question['name'] in headers:
                headers.append(question['name'])
            data_dict[key].append(question['answer'])
    #print(headers)    
    #pprint(data_dict)
    return data_dict, headers


def zip_it(data_dict):
    basic_array = []
    for value in data_dict.values():
        basic_array.append(value)    
    return numpy.array(basic_array)


def analyze(n, np_array):
    kmeans = KMeans(n_clusters=n)
    kmeans.fit(np_array)
    return kmeans


def get_analysis():
    data = read_json("insomnia_data.json")
    #pprint(data)
    data_dict, headers = to_array_dict(data)
    np_array = zip_it(data_dict)
    #pprint(np_array)
    kmeans = analyze(2, np_array)
    centroids = kmeans.cluster_centers_
    ret = []
    for j in range(len(centroids)):
        item = {}
        for i in range(len(headers)):
            item[headers[i]] = str(centroids[j][i])
        ret.append(item)
    #pprint(ret)
    return jsonify(ret)
    


