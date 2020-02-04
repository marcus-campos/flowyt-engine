from .views import (BuildWorkspace, Reload)

urls = [
    {"path": "/_workspaces/build/workspace", "view": BuildWorkspace},
    {"path": "/_workspaces/reload", "view": Reload},
]