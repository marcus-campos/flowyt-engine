from utils.json_parser import parse_json_file

from .views import StartFlow
from orchestrator.settings import SUBDOMAIN_MODE

urls = []

workspaces_urls = parse_json_file("/urls.json")

for url in workspaces_urls:
    url_to_append = {
        "path": url.get("path"),
        "view": StartFlow,
        "methods": [url.get("method").upper()],
        "kwargs": {"workspace": url.get("workspace"), "flow": url.get("flow")},
        "subdomain": url.get("workspace"),
    }

    if not SUBDOMAIN_MODE:
        url_to_append["path"] = "/" + url.get("workspace") + url.get("path")
        del url_to_append["subdomain"]

    urls.append(url_to_append)
