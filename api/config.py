## Config
from os import path, getenv, urandom
from datetime import timedelta

basedir = path.abspath(path.dirname(__file__))


class Config:
    # Change secret keys in production run!
    SECRET_KEY = getenv("SECRET_KEY", urandom(25))
    DEBUG = False

    # Key used for registering users.
    ENTRY_KEY = getenv("ENTRY_KEY", "SpaceyTesting")

    # JWT Configs
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY", urandom(25))
    ## Set token to expire every week
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv(
        "DATABASE_URL", "postgres://postgres:password@localhost:5432/spaceytesting"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = getenv(
        "DATABASE_URL", "postgres://postgres:password@localhost:5432/spacey"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)

key = Config.SECRET_KEY
