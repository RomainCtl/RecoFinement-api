# User Schemas
from src import ma

from src.model import User


class UserMeta:
    model = User


class UserBase(ma.SQLAlchemyAutoSchema):
    class Meta(UserMeta):
        fields = ("uuid", "email", "username")


class UserObject(ma.SQLAlchemyAutoSchema):
    class Meta(UserMeta):
        fields = ("uuid", "email", "username", "meta_user_books",
                  "meta_user_games", "meta_user_applications", "meta_user_tracks")
