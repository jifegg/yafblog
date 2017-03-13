import os
class Config(object):
    DEBUG = False
    TESTING = False
    CHARSET='utf8'
    SECRET_KEY='key'

class ProductionConfig(Config):
    DB='yafblog'
    HOST='127.0.0.1'
    USER='root'
    PASSWORD='123456'

class DevelopmentConfig(Config):
    DB='yafblog'
    HOST='127.0.0.1'
    USER='root'
    PASSWORD='123456'
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}

def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'development')
    app.config.from_object(config[config_name])
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)
