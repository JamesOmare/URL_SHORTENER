import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'bookmarks.db')
    DEBUG = os.environ.get('DEBUG')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SWAGGER = {
        'title': "Bookmarks API",
        'uiversion':3
    }
  
