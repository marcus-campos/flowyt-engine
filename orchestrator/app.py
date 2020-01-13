
import os

from flask import Flask
from flask_restful import Api

from orchestrator.urls import load_urls

app = Flask(__name__)

# App config
app.config.from_object("orchestrator.settings")

api = Api(app)

# Load urls
api = load_urls(api)

if __name__ == "__main__":
    app.run()
