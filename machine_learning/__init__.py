from flask import Flask

app = Flask(__name__)

from .routes import index_ml, funkcion_ml