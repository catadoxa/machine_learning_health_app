#!env/bin/python3


from flask import Flask


app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route("/")
def route():
    return "Hello, world!"


if __name__ == "__main__":
    app.run(debug=True)


