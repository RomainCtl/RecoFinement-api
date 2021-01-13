# Role Schemas
from marshmallow import fields
from src import ma
from src.model import RoleModel
from src.utils import SQLAlchemyAutoSchema


class RoleMeta:
    model = RoleModel


class RoleBase(SQLAlchemyAutoSchema):
    class Meta(RoleModel):
        pass


class RoleObject(RoleBase):
    permission = ma.Nested("PermissionBase", many=True)
