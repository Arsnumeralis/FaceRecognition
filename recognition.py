from facial_recognition import app

# app = Flask(__name__)


# @app.route('/')
# def index_recognition():
#     return {'message': 'Welcome to the FACE!'}


# @app.route('/paulius')
# def function_recognition():
#     print(request.remote_addr)
#     ip_address = request.remote_addr
#     return {'Your IP address': ip_address}

if __name__ == "__main__":
    app.run()

