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
    groups = ma.Nested("GroupBase", many=True)
    invitations = ma.Nested("GroupBase", many=True)
    owned_groups = ma.Nested("GroupBase", many=True)

    class Meta(ProfileMeta):
        fields = ("uuid", "profilename",
                  "groups", "invitations", "owned_groups")


class ProfileFullObject(SQLAlchemyAutoSchema):
    groups = ma.Nested("GroupBase", many=True)
    invitations = ma.Nested("GroupBase", many=True)
    owned_groups = ma.Nested("GroupBase", many=True)

    liked_genres = ma.Nested("GenreBase", many=True)

    linked_services = ma.Nested("ExternalBase", many=True)

    meta_profile_content = ma.Nested("MetaProfileContentItem", many=True)

    class Meta(ProfileMeta):
        fields = ("uuid", "profilename", "groups", "invitations",
                  "owned_groups", "liked_genres", "linked_services", "meta_profile_content")


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
