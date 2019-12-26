import json
from utils.json_parser import parse_json_file
from .views import StartFlow

urls = []

workspaces_urls = parse_json_file('/urls.json')

for url in workspaces_urls:
    urls.append({
        "path": url.get("path"), 
        "view": StartFlow,
        "methods": [url.get("method").upper()],
        "kwargs": {"workspace": url.get("workspace"), "flow": url.get("flow")},
        "subdomain": url.get("workspace")
    })