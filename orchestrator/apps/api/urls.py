import os

from orchestrator.settings import SUBDOMAIN_MODE, WORKSPACES_PATH, WORKSPACE_STORAGE_MODE

from .views import StartFlow, Workspaces
from utils.json_parser import parse_json_file


urls = []

methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "CONNECT", "TRACE"]

if SUBDOMAIN_MODE:
    urls.append(
        {
            "path": "/<string:workspace>/<path:path>",
            "view": StartFlow,
            "methods": methods,
            "subdomain": "<subdomain>",
        }
    )

else:
    if WORKSPACE_STORAGE_MODE == "local":
        urls.append(
            {"path": "/<string:workspace>/<path:path>", "view": StartFlow, "methods": methods,}
        )

    if WORKSPACE_STORAGE_MODE == "redis":
        urls.append(
            {
                "path": "/<string:subdomain>/<string:workspace>/<path:path>",
                "view": StartFlow,
                "methods": methods,
            }
        )
