from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..util.dto import FactsDto

from ..service.user.utils import load_user
from ..service.fact.service import FactsFeedService

api = FactsDto.api


@api.route("/get")
class FactsGet(Resource):
    @api.doc(
        "Get 10 random facts.",
        responses={
            # To be added.
        },
    )
    def get(self):
        """ Get 10 random facts """
        return FactsFeedService.get()


@api.route("/<string:planet_name>")
class FactsGet(Resource):
    @api.doc(
        "Get 10 random facts about a planet",
        responses={
            # To be added.
        },
    )
    def get(self, planet_name):
        """ Get 10 random facts about a planet """
        return FactsFeedService.get_by_planet(planet_name)
