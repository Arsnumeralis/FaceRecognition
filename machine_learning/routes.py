from machine_learning import app
from flask import request

@app.route('/')
def index_ml():
    return {'message': 'Welcome to the FACE!'}


@app.route('/paulius')
def funkcion_ml():
    print(request.remote_addr)
    ip_address = request.remote_addr
    return {'message':'This is the machine learning endpoint.'}
    # return {'Your IP address': ip_address}