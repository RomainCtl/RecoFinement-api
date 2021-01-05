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


class SerieItem(SQLAlchemyAutoSchema):
    permission = ma.Nested("PermissionBase", many=True)

    class Meta(SerieMeta):
        pass
