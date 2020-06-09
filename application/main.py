from application.config import config_by_name
from application.routes import register_routes
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
import os


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.config["JSON_AS_ASCII"] = False
    app.config['CORS_HEADERS'] = 'Content-Type'
    api = Api(app, authorizations=authorizations)
    register_routes(api, app)
    CORS(app, resources={r'/api/*': {'origins': '*'}})
    return app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.app_context().push()

if __name__ == '__main__':
    app.run()