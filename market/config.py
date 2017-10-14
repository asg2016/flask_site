import os


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE = os.path.join(os.path.abspath('.'), 'market.db')


class DebugConfig(Config):
    DEBUG = True
