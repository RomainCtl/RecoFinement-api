# Content Schemas
from marshmallow import fields
from src import ma
from src.model import ContentModel
from src.utils import SQLAlchemyAutoSchema


class ContentMeta:
    model = ContentModel


class ContentBase(SQLAlchemyAutoSchema):
    genres = ma.Nested("GenreBase", many=True)

    class Meta(ContentMeta):
        pass
