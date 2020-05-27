BASE_ROUTE = 'locations'

def register_routes(api, app, root='api'):
    from application.locations.controller import api as locations_api
    api.add_namespace(locations_api, path=f"/{root}/{BASE_ROUTE}")