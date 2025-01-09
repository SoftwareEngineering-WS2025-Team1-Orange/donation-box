import functools
import inspect
import json
from dataclasses import asdict


class Router:
    def __init__(self):
        self._store = {}

    def route(self, event: str):
        def decorator(func):
            print(f"Adding route for {event}")

            sig = inspect.signature(func)
            param_names = list(sig.parameters.keys())

            if not func.__annotations__ or (
                    'return' in func.__annotations__ and (len(func.__annotations__) - 1) != len(param_names)) or (
                    'return' not in func.__annotations__ and len(func.__annotations__) != len(param_names)):
                self._store[event] = func
                return func

            first_arg_name = next(iter(func.__annotations__))
            datatype_to_cast = func.__annotations__[first_arg_name]

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                casted_arg = datatype_to_cast(**args[0])
                ws = args[1:]
                return_value = func(casted_arg, *ws, **kwargs)
                if return_value:
                    return_class = return_value.__class__.__name__
                    ws[0].send(json.dumps({'event': return_class, 'data': asdict(return_value)}))

            self._store[event] = wrapper

            return wrapper

        return decorator
