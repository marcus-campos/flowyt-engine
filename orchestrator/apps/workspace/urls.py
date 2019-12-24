from .views import (Build, BuildDetail)

urls = [
    {"path": "/build", "view": Build},
    {"path": "/build/<build_id>", "view": BuildDetail},
]