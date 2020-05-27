BASE_ROUTE = 'events'

def register_routes(api, app, root='api'):
    from application.events.controller import api as events_api
    api.add_namespace(events_api, path=f"/{root}/{BASE_ROUTE}")