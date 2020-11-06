from simplifier import afyfy
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.route('/afyfy', methods=['POST'])
def hello_world():
    return jsonify(afyfy(request.get_json()))

# @app.route('/summarize', methods=['POST'])
# def hello_world():
#     return jsonify(summarize(request.get_json()))
