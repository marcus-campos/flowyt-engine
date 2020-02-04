from .views import (BuildWorkspace)

urls = [
    {"path": "/_workspaces/build/workspace", "view": BuildWorkspace},
]