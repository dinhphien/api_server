BASE_ROUTE = 'persons'

def register_routes(api, app, root='api'):
    from application.persons.controller import api as persons_api
    api.add_namespace(persons_api, path=f"/{root}/{BASE_ROUTE}")