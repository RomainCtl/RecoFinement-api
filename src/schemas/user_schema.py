# User Schemas
from src import ma

from src.model import UserModel


class UserMeta:
    model = UserModel


class UserBase(ma.SQLAlchemyAutoSchema):
    class Meta(UserMeta):
        fields = ("uuid", "email", "username")


class UserObject(ma.SQLAlchemyAutoSchema):
    groups = ma.Nested("GroupObject", many=True)
    owned_groups = ma.Nested("GroupObject", many=True)

    class Meta(UserMeta):
        fields = ("uuid", "email", "username", "groups", "owned_groups")
