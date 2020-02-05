import uuid

from flask import Flask
from flask_restful import Api

from apps.api.urls import urls as api_urls
from apps.build.urls import urls as build_urls
from apps.setup.urls import urls as setup_urls

urls = [api_urls, build_urls, setup_urls]


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
