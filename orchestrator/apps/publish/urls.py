from .views import Publish, Reload

urls = [
    {"path": "/_engine/publish", "view": Publish},
    {"path": "/_engine/reload", "view": Reload},
]
