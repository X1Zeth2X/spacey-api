from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..util.dto import FactDto

from ..service.user.utils import get_user
from ..service.fact.service import FactService

api = FactDto.api
_payload = FactDto.create_fact


@api.route("/<string:fact_public_id>")
class FactGet(Resource):
    @api.doc(
        "Get a specific fact using its public id.",
        responses={
            # To be added
        },
    )
    def get(self, fact_public_id):
        return FactService.get(fact_public_id)


@api.route("/create")
class FactCreate(Resource):
    @api.expect(_payload, validate=True)
    @api.doc(
        "Add a new fact.",
        responses={
            # To be added
        },
    )
    @jwt_required
    def post(self):
        current_user = get_user(get_jwt_identity())
        data = request.get_json()
        return FactService.create(data, current_user)


@api.route("/delete/<string:fact_public_id>")
class FactDelete(Resource):
    @api.doc(
        "Delete a specific fact using its public id.",
        responses={
            # To be added
        },
    )
    def delete(self, fact_public_id):
        current_user = get_user(get_jwt_identity())
        return FactService.delete(fact_public_id, current_user)


@api.route("/update/<string:fact_public_id>")
class FactUpdate(Resource):
    @api.doc("Delete a specific fact using its public id.")
    def put(self, fact_public_id):
        current_user = get_user(get_jwt_identity())
        data = request.get_json()
        return FactService.update(fact_public_id, data, current_user)
