## Main

import logging

from os import getenv
from flask import Flask

# Import extensions
from .extensions import db, ma, jwt, bcrypt, cors, limiter

# Import configuration
from api.config import config_by_name, basedir

# Static path
static_url_path = basedir + "/static"


def create_app(config_name):
    app = Flask(__name__, static_url_path=static_url_path)
    app.config.from_object(getenv('APP_SETTINGS', config_by_name[config_name]))

    ## Add logger
    logging.basicConfig(
        filename="api.log",
        level=logging.NOTSET,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    )

    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    limiter.limit(app)
