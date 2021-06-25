from flask import Flask, request 

app = Flask(__name__)


@app.route('/')
def index():
    return {'message': 'Welcome to the FACE!'}


@app.route('/paulius', methods=["GET"])
def funkcija():
    print(request.remote_addr)
    ip_address = request.remote_addr
    return {'Jusu IP adresas': ip_address}

