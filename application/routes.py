def register_routes(api, app, root="api"):
    from application.news import register_routes as attach_news
    from application.agreements import register_routes as attach_agreements
    from application.countries import register_routes as attach_countries
    from application.events import register_routes as attach_events
    from application.locations import register_routes as attach_locations
    from application.organizations import register_routes as attach_organizations
    from application.persons import register_routes as attach_persons
    from application.times import register_routes as attach_times




    # Add routes
    attach_news(api, app)
    attach_agreements(api, app)
    attach_countries(api, app)
    attach_events(api, app)
    attach_locations(api, app)
    attach_organizations(api, app)
    attach_persons(api, app)
    attach_times(api, app)

