class Router:
    def __init__(self):
        self.store = {}

    def route(self, event: str):
        def decorator(func):
            print(f"Adding route for {event}")
            self.store[event] = func
            return func

        return decorator
