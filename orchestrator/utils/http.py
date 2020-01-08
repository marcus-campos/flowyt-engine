import json
import uuid

import requests


class HttpRequest:
    def __init__(self, url):
        self.url = url

    def __get_default_headers(self, headers):
        default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Request-ID": str(uuid.uuid4()),
        }

        return {**default_headers, **headers}

    def get(self, *args, **kwargs):
        url = self.url
        headers = self.__get_default_headers(kwargs.get("headers", {}))
        params = kwargs.get("params", {})
        response = requests.get(url=url, params=params, headers=headers)
        return response

    def post(self, *args, **kwargs):
        url = self.url
        headers = self.__get_default_headers(kwargs.get("headers", {}))
        data = kwargs.get("data", {})
        
        if headers.get("Content-Type") == "application/json":
            data = json.dumps(data)

        #TODO: Support multipart files upload

        response = requests.post(url=url, data=data, headers=headers)
        return response

    def put(self, *args, **kwargs):
        url = self.url
        headers = self.__get_default_headers(kwargs.get("headers", {}))
        data = kwargs.get("data", {})

        if headers.get("Content-Type") == "application/json":
            data = json.dumps(data)

        response = requests.put(url=url, data=data, headers=headers)
        return response

    def delete(self, *args, **kwargs):
        url = self.url
        headers = self.__get_default_headers(kwargs.get("headers", {}))
        response = requests.delete(url=url, headers=headers)
        return response

    def patch(self, *args, **kwargs):
        url = self.url
        headers = self.__get_default_headers(kwargs.get("headers", {}))
        data = kwargs.get("data", {})

        if headers.get("Content-Type") == "application/json":
            data = json.dumps(data)

        response = requests.patch(url=url, data=data, headers=headers)
        return response
