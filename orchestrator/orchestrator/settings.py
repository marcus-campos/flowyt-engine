import os

# Load env
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_PATH = BASE_DIR + "/../../.env"

# Load env file
load_dotenv(dotenv_path=ENV_PATH)


########################################
##             SETTINGS               ##
########################################

# System
ENV = os.getenv("SYS_APP_ENV", "production")
DEBUG = os.getenv("SYS_APP_DEBUG", "false").lower() == "true"

SECRET_KEY = os.getenv("APP_SECRET_KEY", "")

if os.getenv("APP_HOST", None) and os.getenv("APP_PORT", None):
    HOST = os.getenv("APP_HOST", "127.0.0.1")
    PORT = os.getenv("APP_PORT", "5000")
    SERVER_NAME = "{0}:{1}".format(HOST.replace("https://", "").replace("http://", ""), PORT)

# Apps
UPLOAD_FOLDER = BASE_DIR + "/../../storage"
STORAGE_FOLDER_TEMP_UPLOADS = UPLOAD_FOLDER + "/temp/uploads"

WORKSPACES_DIR = "/../../workspaces"
WORKSPACES_PATH = BASE_DIR + WORKSPACES_DIR
SUBDOMAIN_MODE = os.getenv("SUBDOMAIN_MODE", "false").lower() == "true"
