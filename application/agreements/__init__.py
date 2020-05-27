BASE_ROUTE = 'agreements'

def register_routes(api, app, root='api'):
    from application.agreements.controller import api as agreements_api
    api.add_namespace(agreements_api, path=f"/{root}/{BASE_ROUTE}")