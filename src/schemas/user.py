# User Schemas
from src import ma

from src.model import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("uuid", "username", "email")
