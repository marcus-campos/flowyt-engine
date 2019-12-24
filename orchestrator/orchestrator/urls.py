from flask import Flask
from flask_restful import Api

from apps.api.urls import urls as api_urls
from apps.workspace.urls import urls as workspace_urls

urls = [
    api_urls,
    workspace_urls
]

def load_urls(api):
    for url in urls:
        for view in url:
            api.add_resource(
                view.get("view"), 
                view.get("path"), 
                methods=view.get("methods"), 
                resource_class_kwargs=view.get("kwargs")
            )
    
    return api
