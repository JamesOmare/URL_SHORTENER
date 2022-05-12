from tkinter import SW
from flask import Flask
from .auth.views import auth
from .bookmarks.views import bookmarks
from .utils import db, jwt_manager, swagger
from .models.bookmark import Bookmark
from .config.config import Config
from werkzeug.exceptions import NotFound, MethodNotAllowed
from .config.swagger import template, swagger_config
from flasgger import Swagger


def create_app(config = Config):

    #instance relative config tells our flask application that
    #there will be some configurations set up outside the directory
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    db.init_app(app)
    jwt_manager.init_app(app)
    Swagger(app, config = swagger_config, template = template)
    
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    

    @app.errorhandler(NotFound)
    def not_found(error):
        return {'error': 'Not Found'}, 404

    @app.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {'error': 'Method Not Allowed'}, 405


    

    return app