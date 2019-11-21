from flask_restplus import Api
from flask import Blueprint

# Import controllers

blueprint = Blueprint("api", __name__)

api = Api(blueprint, title="NAQL's API with JWT", version="0.1",)

# api.add_namespace(ns, path='/path' *optional)
