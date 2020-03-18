import os

from orchestrator.settings import SUBDOMAIN_MODE, WORKSPACES_PATH

from .views import StartFlow, Workspaces
from utils.json_parser import parse_json_file

urls = []

path = WORKSPACES_PATH
dirlist = [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]

for workspace_name in dirlist:
    workspace_routes = parse_json_file("{0}/{1}/routes.json".format(path, workspace_name))

    for url in workspace_routes:
        url_to_append = {
            "path": url.get("path"),
            "view": StartFlow,
            "methods": [url.get("method").upper()],
            "kwargs": {"workspace": workspace_name, "flow": url.get("flow")},
            "subdomain": workspace_name,
        }

        if not SUBDOMAIN_MODE:
            url_to_append["path"] = "/" + workspace_name + url.get("path")
            del url_to_append["subdomain"]

        urls.append(url_to_append)

urls.append(
    {
        "path": "/_engine/workspaces/routes",
        "view": Workspaces,
        "methods": ["GET"],
        "kwargs": {"workspaces_urls": urls.copy()},
    }
)
