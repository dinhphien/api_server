BASE_ROUTE = 'times'

def register_routes(api, app, root='api'):
    from application.times.controller import api as times_api
    api.add_namespace(times_api, path=f"/{root}/{BASE_ROUTE}")