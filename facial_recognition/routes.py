from facial_recognition import app
from flask import request

@app.route('/')
def index_recognition():
    return {'message': 'Welcome to the FACE!'}


@app.route('/paulius')
def function_recognition():
    print(request.remote_addr)
    ip_address = request.remote_addr
    return {'message': 'This is the facial recognition endpoint'}
    # return {'Your IP address': ip_address}
