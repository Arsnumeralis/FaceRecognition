from flask import Flask

app = Flask(__name__)

from .routes import index_recognition, function_recognition