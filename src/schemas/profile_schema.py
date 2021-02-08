# Profile Schemas
from src import ma

from src.model import ProfileModel
from src.utils import SQLAlchemyAutoSchema, DTOSchema

# Validations with Marshmallow
from marshmallow import fields
from marshmallow.validate import Regexp, Length

# Validations with Marshmallow
from marshmallow import fields
from marshmallow.validate import Regexp, Length

from src.utils import DTOSchema


class ProfileMeta:
    model = ProfileModel


class ProfileBase(SQLAlchemyAutoSchema):

    class Meta(ProfileMeta):
        fields = ("uuid", "profilename")


class ProfileObject(SQLAlchemyAutoSchema):
    liked_genres = ma.Nested("GenreBase", many=True)

    class Meta(ProfileMeta):
        fields = ("uuid", "profilename", "liked_genres")


class UpdateProfileDataSchema(DTOSchema):
    """ /auth/register  [POST]
        /profile/update    [PATCH]

    Parameters:
    - Profilename (Str)
    """
    profilename = fields.Str(
        validate=[
            Length(min=4, max=15),
            Regexp(
                r"^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$",
                error="Invalid profilename!",
            ),
        ],
    )
