import json
from orchestrator.settings import (BASE_DIR, WORKSPACES_DIR)
from .views import StartFlow

urls = []

with open(BASE_DIR + WORKSPACES_DIR + "/urls.json", 'r') as f:
    workspaces_urls = json.load(f)

for url in workspaces_urls:
    urls.append({
        "path": url.get("path"), 
        "view": StartFlow,
        "methods": [url.get("method").upper()],
        "kwargs": {"workspace": url.get("workspace"), "flow": url.get("flow")}
    })