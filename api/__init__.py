from flask_restplus import Api
from flask import Blueprint

# Import controllers here
from .auth.controller import api as auth_ns

from .main.controller.user_controller import api as user_ns
from .main.controller.fact_controller import api as fact_ns
from .main.controller.facts_controller import api as facts_ns


blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="API with JWT",
    version="0.1",
    description="The coolest Flask RESTPlus boilerplate ever.",
)

# api.add_namespace(namespace, path='/path' )
api.add_namespace(user_ns)

api.add_namespace(auth_ns)

api.add_namespace(fact_ns)
api.add_namespace(facts_ns)