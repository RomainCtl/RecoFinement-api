# User Schemas
from src import ma

from src.model import UserModel
from src.utils import SQLAlchemyAutoSchema

# Validations with Marshmallow
from marshmallow import fields
from marshmallow.validate import Regexp, Length, Email

from src.utils import DTOSchema


class UserMeta:
    model = UserModel


class UserBase(SQLAlchemyAutoSchema):
    class Meta(UserMeta):
        fields = ("uuid", "email", "username")


class UserObject(SQLAlchemyAutoSchema):
    groups = ma.Nested("GroupBase", many=True)
    invitations = ma.Nested("GroupBase", many=True)
    owned_groups = ma.Nested("GroupBase", many=True)

    class Meta(UserMeta):
        fields = ("uuid", "email", "username", "groups",
                  "invitations", "owned_groups")

class UpdateUserDataSchema(DTOSchema):
    """ /auth/register [POST]

    Parameters:
    - Email
    - Username (Str)
    - Password (Str)
    """

    email = fields.Email(validate=[Length(min=5,max=64)])
    username = fields.Str(
        validate=[
            Length(min=4, max=15),
            Regexp(
                r"^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$",
                error="Invalid username!",
            ),
        ],
    )
    password = fields.Str(
        validate=[
            Length(min=8, max=128),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}",
                error="Password must contain at least minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character !"
            ),
        ],
    )