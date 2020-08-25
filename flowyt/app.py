import os
import sys

from flask import Flask
from flask_restful import Api

from flowyt.urls import load_urls

from utils.splash import loading

app = Flask(__name__)

# App config
app.config.from_object("flowyt.settings")

api = Api(app)

# Load urls
api = load_urls(api)

if __name__ == "__main__":
    loading(app.config)
    cli = sys.modules["flask.cli"]
    cli.show_server_banner = lambda *x: None
    app.run()
