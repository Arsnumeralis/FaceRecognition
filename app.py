from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return {'message': 'Welcome to the FACE!'}


@app.route('/paulius')
def funkcija():
    return {'dantys': '32'}