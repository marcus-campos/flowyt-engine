from .views import (BuildWorkspace, Reload)

urls = [
    {"path": "/_engine/build/workspace", "view": BuildWorkspace},
    {"path": "/_engine/reload", "view": Reload},
]