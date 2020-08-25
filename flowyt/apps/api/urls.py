import os

from flowyt.settings import SUBDOMAIN_MODE, WORKSPACE_STORAGE_MODE, WORKSPACES_PATH

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
            "subdomain": "<__subdomain__>",
        }
    )

else:
    if WORKSPACE_STORAGE_MODE == "local":
        urls.append(
            {"path": "/_engine/routes", "view": Workspaces, "methods": ["GET"],}
        )

        urls.append(
            {"path": "/<string:workspace>/<path:path>", "view": StartFlow, "methods": methods,}
        )

    if WORKSPACE_STORAGE_MODE == "redis":
        urls.append(
            {
                "path": "/<string:__subdomain__>/<string:workspace>/<path:path>",
                "view": StartFlow,
                "methods": methods,
            }
        )
