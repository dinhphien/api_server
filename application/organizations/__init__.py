BASE_ROUTE = 'organizations'

def register_routes(api, app, root='api'):
    from application.organizations.controller import api as organizations_api
    api.add_namespace(organizations_api, path=f"/{root}/{BASE_ROUTE}")