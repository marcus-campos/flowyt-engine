import os
from distutils import util

# Load env
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = BASE_DIR + "/../"
ROOT_DIR = PROJECT_DIR + "/../"
ENV_PATH = ROOT_DIR + ".env"

# Load env file
load_dotenv(dotenv_path=ENV_PATH)


########################################
##          SETTINGS SYSTEM           ##
########################################

ENV = os.getenv("SYS_APP_ENV", "production")
DEBUG = os.getenv("SYS_APP_DEBUG", "false").lower() == "true"
SECRET_KEY = os.getenv("APP_SECRET_KEY", "")

SERVER_NAME = "127.0.0.1:80"
if os.getenv("APP_HOST", None) and os.getenv("APP_PORT", None):
    HOST = os.getenv("APP_HOST", "127.0.0.1")
    PORT = os.getenv("APP_PORT", "5000")
    SERVER_NAME = "{0}:{1}".format(HOST.replace("https://", "").replace("http://", ""), PORT)


########################################
##          SETTINGS APP           ##
########################################
SUBDOMAIN_MODE = bool(util.strtobool(os.getenv("SUBDOMAIN_MODE", "false")))
WORKSPACE_STORAGE_MODE = os.getenv("WORKSPACE_STORAGE_MODE", "local")  # local, redis

# Workspace storage mode local
UPLOAD_FOLDER = ROOT_DIR + "storage"
STORAGE_FOLDER_TEMP_UPLOADS = UPLOAD_FOLDER + "/temp/uploads"
WORKSPACES_DIR = "workspaces"
WORKSPACES_PATH = ROOT_DIR + WORKSPACES_DIR

# Workspace storage mode redis
REDIS = {
    "WORKSPACE": {
        "HOST": os.getenv("REDIS_WORKSPACE_HOST", "127.0.0.1"),
        "PORT": os.getenv("REDIS_WORKSPACE_PORT", 6379),
        "PASSWORD": os.getenv("REDIS_WORKSPACE_PASSWORD"),
        "DB": os.getenv("REDIS_WORKSPACE_DB", 0),
    },
    "QUOTA": {
        "HOST": os.getenv("REDIS_QUOTA_HOST", "127.0.0.1"),
        "PORT": os.getenv("REDIS_QUOTA_PORT", 6379),
        "PASSWORD": os.getenv("REDIS_QUOTA_PASSWORD"),
        "DB": os.getenv("REDIS_QUOTA_DB", 0),
    },
}

ASYNC_MAX_CONCURRENCE = int(os.getenv("ASYNC_MAX_CONCURRENCE", 10))
