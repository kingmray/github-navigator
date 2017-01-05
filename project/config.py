import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
	"""Base configuration"""
	pass

class DevelopmentConfig(BaseConfig):
	"""Development configuration"""
	DEBUG = True