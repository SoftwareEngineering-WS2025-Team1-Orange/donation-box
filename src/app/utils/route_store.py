class RouteStore:
    def __init__(self):
        self.routes = []

    def add_route(self, route):
        self.routes.append(route)

    def get_routes(self):
        return self.routes

    def get_route(self, route_id):
        for route in self.routes:
            if route.route_id == route_id:
                return route
        return None

    def remove_route(self, route_id):
        for route in self.routes:
            if route.route_id == route_id:
                self.routes.remove(route)
                return
        return None

    def update_route(self, route_id, route):
        for i, r in enumerate(self.routes):
            if r.route_id == route_id:
                self.routes[i] = route
                return
        return None

    def __str__(self):
        return str(self.routes)


route_store = RouteStore()
