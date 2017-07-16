#!../env/bin/python


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


@app.route("/api/test", methods=["POST"])
def test():
    data = {"data": "data"}
    url = "http://127.0.0.1:5000/api/ml_data"
    parsed = json.dumps(data).encode("utf8")
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    req = urllib.request.Request(url, parsed, headers)
    resp = urllib.request.urlopen(req)
    return resp.read()



if __name__ == "__main__":
    app.run(debug=True, port=5001)


