from .views import Info, Ping, Setup

urls = [
    {"path": "/_engine/setup", "view": Setup},
    {"path": "/_engine/ping", "view": Ping, "methods": ["GET"]},
    {"path": "/_engine/info", "view": Info, "methods": ["GET"]},
]
