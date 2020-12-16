from src import db
from src.utils import GUID

RolePermissionModel = db.Table("role_permission",
                            db.Column("role_id", db.Integer, db.ForeignKey(
                                "role.track_id"), primary_key=True),
                            db.Column("permission", db.String(45), db.ForeignKey(
                                "permission.permission"), primary_key=True)
                            )

class RoleModel(db.Model):
    """
    Role Model for storing different roles
    """
    __tablename__ = "role"

    role_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    name = db.Column(db.String(45))

    permission = db.relationship(
        "PermissionModel", secondary=RolePermissionModel, lazy="dynamic")

class PermissionModel(db.Model):
    """
    Permission Model for storing all role's permission
    """
    __tablename__ = "permission"

    permission = db.Column(db.String(45), primary_key=True,
                            autoincrement=True, nullable=False)

    
