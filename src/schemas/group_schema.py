from marshmallow import fields
from marshmallow.validate import Regexp, Length

from src import ma
from src.model import GroupModel
from src.utils import DTOSchema


class GroupMeta:
    model = GroupModel


class GroupBase(ma.SQLAlchemyAutoSchema):
    class Meta(GroupMeta):
        pass


class GroupObject(ma.SQLAlchemyAutoSchema):
    invitations = ma.Nested("UserBase", many=True)
    members = ma.Nested("UserBase", many=True)
    owner = ma.Nested("UserBase")

    class Meta(GroupMeta):
        pass


class GroupCreateSchema(DTOSchema):
    """ /group [POST]

    Parameters:
    - name (Str)
    """

    name = fields.Str(
        required=True,
        validate=[
            Length(min=3, max=45),
            Regexp(
                r"^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$",
                error="Invalid name!",
            ),
        ],
    )


class GroupAddMemberSchema(DTOSchema):
    """ /group/<string:group_uuid> [PUT]

    Parameters:
    - uuid (UUID)
    """

    uuid = fields.UUID(required=True)
