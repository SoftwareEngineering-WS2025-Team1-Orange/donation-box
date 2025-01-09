import functools


class Router:
    def __init__(self):
        self._store = {}

    def route(self, event: str):
        def decorator(func):
            print(f"Adding route for {event}")

            if not func.__annotations__ or len(func.__annotations__) != len(func.__code__.co_varnames):
                self._store[event] = func
                return func

            first_arg_name = next(iter(func.__annotations__))
            datatype_to_cast = func.__annotations__[first_arg_name]

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                casted_arg = datatype_to_cast(args[0])
                return func(casted_arg, *args[1:], **kwargs)

            self._store[event] = wrapper

            return wrapper

        return decorator
