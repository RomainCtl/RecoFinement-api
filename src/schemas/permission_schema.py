# Permission Schemas
from marshmallow import fields
from src import ma
from src.model import PermissionModel
from src.utils import SQLAlchemyAutoSchema


class PermissionMeta:
    model = PermissionModel


class PermissionBase(SQLAlchemyAutoSchema):
    class Meta(PermissionModel):
        pass


class PermissionItem(SQLAlchemyAutoSchema):
    class Meta(PermissionModel):
        pass
