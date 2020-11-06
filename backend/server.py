from simplifier import afyfy
from flask import Flask, request
app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.route('/afyfy', methods=['POST'])
def hello_world():
    return afyfy(request.form['text'])
