from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..util.dto import FactsDto

from ..service.user.utils import load_user
from ..service.fact.service import FactsFeedService

api = FactsDto.api


@api.route("/get")
class FactGet(Resource):
    @api.doc("Get a specific fact using its public id.", responses={
      # To be added.
    })
    def get(self):
        """ Get random 10 facts """
        return FactsFeedService.get()
