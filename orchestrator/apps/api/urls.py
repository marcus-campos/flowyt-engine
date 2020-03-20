import os

from orchestrator.settings import SUBDOMAIN_MODE, WORKSPACES_PATH, WORKSPACE_STORAGE_MODE

from .views import StartFlow, Workspaces
from utils.json_parser import parse_json_file


urls = []

urls.append(
    {
        "path": "/<string:workspace>/<path:path>",
        "view": StartFlow,
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "CONNECT", "TRACE"],
        "subdomain": "<subdomain>",
    }
)
