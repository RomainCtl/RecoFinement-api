# User Schemas
from src import ma

from src.model import UserModel
from src.utils import SQLAlchemyAutoSchema


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
