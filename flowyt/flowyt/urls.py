import uuid

from flask import Flask
from flask_restful import Api

from apps.api.urls import urls as api_urls
from apps.publish.urls import urls as publish_urls
from apps.manager.urls import urls as manager_urls

urls = [api_urls, publish_urls, manager_urls]


def load_urls(api):
    for url in urls:
        for view in url:
            endpoint_name = str(uuid.uuid4())
            api.add_resource(
                view.get("view"),
                view.get("path"),
                methods=view.get("methods", None),
                resource_class_kwargs=view.get("kwargs", {}),
                subdomain=view.get("subdomain", None),
                endpoint=endpoint_name,
            )

    return api
