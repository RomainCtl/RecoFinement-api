# Book Schemas
from marshmallow import fields
from src import ma
from src.model import BookModel
from src.utils import SQLAlchemyAutoSchema


class BookMeta:
    model = BookModel
    include_fk = True


class BookBase(SQLAlchemyAutoSchema):
    rating = fields.Function(lambda obj: obj.content.rating)
    rating_count = fields.Function(lambda obj: obj.content.rating_count)
    popularity_score = fields.Function(
        lambda obj: obj.content.popularity_score)

    class Meta(BookMeta):
        pass


class BookExtra(BookBase):
    # Extra fields from join with 'recommended_application'
    reco_engine = fields.String(attribute="engine", default=None)
    reco_score = fields.Float(attribute="score", default=None)
