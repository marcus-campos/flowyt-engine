from werkzeug.routing import Map, Rule, NotFound, RequestRedirect


class Router:
    urls_map = []
    server_name = ""

    def __init__(self, server_name, subdomain, routes):
        self.urls_map = self.__map(routes)
        self.server_name = server_name

    def __map(self, routes):
        urls = []
        for route in routes:
            urls.append(
                Rule(
                    route["path"],
                    endpoint=route["flow"],
                    methods=[route["method"]],
                )
            )

        return Map(urls)

    def match(self, path, workspace, method):
        urls = self.urls_map.bind(self.server_name, workspace)
        flow = urls.match(path, method)
        return flow[0]
