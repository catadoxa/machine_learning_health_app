#!env/bin/python


from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import urllib
import json


app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route("/api/ml_data", methods=["POST"])
def ml_data():
    data = {"newstuff": "new!"}
    res = request.get_json(force=True)
    print(res)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)


