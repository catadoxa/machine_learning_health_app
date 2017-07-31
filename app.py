#!/usr/bin/env python


from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import urllib
import json
from analysis.analyze import get_analysis

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


#@app.route("/api/login", methods=["POST"])
#def login():
#    data = read_json("insomnia_questions.json")
#    req = request.get_json(force=True)
#    return jsonify(data)



@app.route("/api/ml_data", methods=["POST"])
def ml_data():
    data = get_analysis()
    req = request.get_json(force=True)
    #print(data)
    return data


if __name__ == "__main__":
    app.run(debug=True)


