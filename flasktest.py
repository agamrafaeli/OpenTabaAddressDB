#!/usr/bin/python
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/moo", methods=['GET'])
def moo():
    return "MOO %s" % request.args.get('k','')

if __name__ == "__main__":
    app.run()
