#!/usr/bin/env python


from flask import Flask
from flask import request
import json
from flask import jsonify
from analysis.analyze import get_analysis
import requests


app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route("/api/ml_data", methods=["POST"])
def ml_data():
    try:
        req = request.get_json(force=True)
        req = dict(req)
        #data = "analysis/insomnia_data.json"
        url = "http://web.engr.oregonstate.edu/~aluyorg/history.php"
        payload = {"username": req["user"], "password": req["password"]}
        r = requests.get(url, params=payload)
        data = r.json()
        data = get_analysis(data)
    except:
        data = {"error": "true"}
        data = jsonify(data)
    return data


if __name__ == "__main__":
    app.run()


