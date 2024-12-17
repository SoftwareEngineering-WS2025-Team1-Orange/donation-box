class RouteStore:
    def __init__(self):
        self.routes = {}

    def add_route(self, event, func):
        self.routes[event] = func

    def get_route(self, event):
        return self.routes.get(event)

    def __str__(self):
        return str(self.routes)


route_store = RouteStore()
