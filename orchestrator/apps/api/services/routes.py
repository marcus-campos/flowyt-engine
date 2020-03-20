from werkzeug.routing import Map, Rule, NotFound, RequestRedirect


class Router():
    urls_map = []
    server_name = ""
    subdomain = ""

    def __init__(self, server_name, subdomain, routes):
        self.urls_map = self.__map(routes)
        self.server_name = server_name
        self.subdomain = subdomain

    def __map(self, routes):
        urls = []
        for route in routes:
            if self.subdomain == "":
                urls.append(Rule(route["path"], endpoint=route["flow"], methods=[route["method"]]))
                continue

            urls.append(Rule(route["path"], endpoint=route["flow"], subdomain=route["subdomain"], methods=[route["method"]]))

        return Map(urls)

    def match(self, path, workspace, method):
        urls = self.urls_map.bind(self.server_name, workspace, self.subdomain)

        try:
            return urls.match(path, method)
        except Exception as e:
            return False
    
