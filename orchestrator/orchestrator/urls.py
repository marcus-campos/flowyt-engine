from flask import Flask
from flask_restful import Api

from apps.api.urls import urls as api_urls

urls = [
    api_urls
]

def load_urls(api):
    # Load routes
    for url in urls:
        for view in url:
            api.add_resource(view.get("view"), view.get("path"))
    
    return api
