from marshmallow import fields

from src import ma
from src.model import GenreModel
from src.utils import SQLAlchemyAutoSchema


class GenreMeta:
    model = GenreModel


class GenreBase(SQLAlchemyAutoSchema):
    content_type = fields.Method("get_content_type")

    def get_content_type(self, obj):
        return obj.content_type.value

    class Meta(GenreMeta):
        pass


class GenreObject(SQLAlchemyAutoSchema):
    linked_genres = ma.Nested("GenreBase", many=True)
    content_type = fields.Method("get_content_type")

    def get_content_type(self, obj):
        return obj.content_type.value

    class Meta(GenreMeta):
        pass
