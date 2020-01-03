from flask import request
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
        """ Get random facts """
        limit = request.args.get("limit", default=100, type=int)
        return FactsFeedService.get(limit)


@api.route("/<string:planet_name>")
class FactsGet(Resource):
    @api.doc(
        "Get 10 random facts about a planet",
        responses={
            # To be added.
        },
    )
    def get(self, planet_name):
        """ Get random facts about a planet """
        limit = request.args.get("limit", default=100, type=int)
        return FactsFeedService.get_by_planet(planet_name, limit)
