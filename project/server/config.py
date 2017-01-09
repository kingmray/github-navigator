import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    """Base configuration"""
    pass

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    # This information is obtained upon registration of a new GitHub OAuth
    # application here: https://github.com/settings/applications/new
