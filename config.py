class Config(object):
    DEBUG = False
    TESTING = False
    CHARSET='utf8'
    SECRET_KEY='key'

class ProductionConfig(Config):
    DB='yafblog',
    HOST='127.0.0.1',
    USER='root',
    PASSWORD='123456',

class DevelopmentConfig(Config):
    DB='yafblog'
    HOST='127.0.0.1'
    USER='root'
    PASSWORD='123456'
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
