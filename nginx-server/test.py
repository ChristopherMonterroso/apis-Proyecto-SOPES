import flask 
from flask import request, jsonify
import json
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/test', methods=['GET'])
def home():
    return "<h1>Hello World</h1>"

if __name__ == '__main__':
    app.run( port=5001)
