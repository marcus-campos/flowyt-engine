import os

# Load env
from dotenv import load_dotenv

# Load env file
env_path = os.getcwd() + "/orchestrator/.env"
load_dotenv(dotenv_path=env_path)


########################################
##             SETTINGS               ##
########################################

# System
ENV = os.getenv("APP_ENV", "development")
SECRET_KEY = os.getenv("APP_SECRET_KEY", "")
DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
# SERVER_NAME = os.getenv("APP_SERVER_NAME", "127.0.0.1:5000")

# Apps
BASE_DIR = os.getcwd()
WORKSPACES_DIR = os.getenv("WORKSPACES_DIR", "/workspaces")
WORKSPACES_PATH = BASE_DIR + WORKSPACES_DIR
SUBDOMAIN_MODE = os.getenv("WORKSPACES_DIR", "false").lower() == "true"
