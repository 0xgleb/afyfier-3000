from simplifier import afyfy
from flask import Flask, request
app = Flask(__name__)

@app.route('/afyfy', methods=['POST'])
def hello_world():
    return afyfy(request.form['text'])
