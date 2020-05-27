BASE_ROUTE = 'countries'

def register_routes(api, app, root='api'):
    from application.countries.controller import api as countries_api
    api.add_namespace(countries_api, path=f"/{root}/{BASE_ROUTE}")