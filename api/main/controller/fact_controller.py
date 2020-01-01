from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..util.dto import FactDto

from ..service.user.utils import load_user
from ..service.fact.service import FactService

api = FactDto.api
_payload = FactDto.create_fact


@api.route("/get/<string:fact_public_id>")
class FactGet(Resource):
    @api.doc("Get a specific fact using its public id.", responses={})
    @jwt_required
    def get(self, fact_public_id):
        """ """
        pass


@api.route("/create")
class FactCreate(Resource):
    @api.expect(_payload, validate=True)
    @api.doc("Add a new fact.", responses={})
    @jwt_required
    def post(self):
        current_user = load_user(get_jwt_identity())
        data = request.get_json()
        return FactService.create(data, current_user)
