from flask import Flask
from flask_restful import Api

from orchestrator.urls import load_urls
from orchestrator.settings import SERVER_NAME

app = Flask(__name__)

# App configs
app.config["SERVER_NAME"] = SERVER_NAME

api = Api(app)
# Load urls
api = load_urls(api)

if __name__ == '__main__':
    app.run(debug=True)