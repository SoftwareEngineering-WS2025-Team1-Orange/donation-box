from bright_ws import Router


auth_router = Router()


@auth_router.route(event="authResponse")
def authenticate_response(message):
    print(message)
    pass
