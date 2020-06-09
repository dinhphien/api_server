BASE_ROUTE = 'auth'

def register_routes(api, app, root='api'):
    from application.auth.controller import api as auth_api
    api.add_namespace(auth_api, path=f"/{root}/{BASE_ROUTE}")