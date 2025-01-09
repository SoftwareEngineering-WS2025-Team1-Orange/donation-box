from bright_ws import Router
from dclasses import AuthResponse


auth_router = Router()


@auth_router.route(event="authResponse")
def authenticate_response(message):
    print(message)
    return
    parsed_request = AuthResponse(**message)
    if not parsed_request.success:
        print("Not Authenticated")
        exit(1)
    else:
        print("Authenticated")
    pass