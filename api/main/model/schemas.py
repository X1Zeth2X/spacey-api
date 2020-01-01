# Schemas file
from api.main import ma

from .user import User
from .fact import Fact


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class FactSchema(ma.ModelSchema):
    class Meta:
        model = Fact
