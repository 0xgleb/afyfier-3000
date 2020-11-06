from flask import Flask, request
app = Flask(__name__)

@app.route('/afyfier', methods=['POST'])
def hello_world():
    return request.form['text']
