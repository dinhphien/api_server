BASE_ROUTE = 'news'

def register_routes(api, app, root='api'):
    from application.news.controller import api as news_api

    api.add_namespace(news_api, path=f"/{root}/{BASE_ROUTE}")