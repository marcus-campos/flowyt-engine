from .views import Setup, Ping, Info


urls = [
    {"path": "/_engine/setup", "view": Setup},
    {"path": "/_engine/ping", "view": Ping, "methods": ["GET"]},
    {"path": "/_engine/info", "view": Info, "methods": ["GET"]},
]
