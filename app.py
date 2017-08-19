#!/usr/bin/env python


from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import urllib
import json
from analysis.analyze import get_analysis
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#@app.after_request
#def after_request(response):
#    response.headers.add('Access-Control-Allow-Origin', '*')
#    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#    return response

@cross_origin()
@app.route("/api/ml_data", methods=["POST"])
def ml_data():
    req = request.get_json(force=True)
    req = dict(req)
#    data = "analysis/insomnia_data.json"
    url = "http://web.engr.oregonstate.edu/~aluyorg/history.php"
    url = "{}?username={}&password={}".format(url, req["user"], req["password"])
    url = "https://www-eng-x.llnl.gov/documents/a_document.txt"
    req_data = json.dumps(req).encode("utf8")
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    req = urllib.request.Request(url, req_data, headers)
    resp = urllib.request.urlopen(req)
#    resp = urllib.request.urlopen(url)
#    data = json.loads(resp.read())
#    data = get_analysis(data)
    data = resp.read()
    print(data)
    return data


if __name__ == "__main__":
    app.run(debug=True)


