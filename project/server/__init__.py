import os

################
#### config ####
################

from flask import Flask

app = Flask(
    __name__,
    template_folder='../client/templates',
    static_folder='../client/static'
)

app_settings = os.getenv('APP_SETTINGS', 'project.server.config.DevelopmentConfig')
app.config.from_object(app_settings)
app.secret_key = os.urandom(24)

###################
### blueprints ####
###################

from project.server.main.views import main_blueprint
app.register_blueprint(main_blueprint)
