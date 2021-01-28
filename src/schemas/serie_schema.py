# Serie Schemas
from marshmallow import fields
from src import ma
from src.model import SerieModel, SerieAdditionalModel
from src.utils import SQLAlchemyAutoSchema
from .genre_schema import GenreBase


class SerieMeta:
    model = SerieModel
    include_fk = True


class SerieBase(SQLAlchemyAutoSchema):
    rating = fields.Function(lambda obj: obj.content.rating)
    rating_count = fields.Function(lambda obj: obj.content.rating_count)
    popularity_score = fields.Function(
        lambda obj: obj.content.popularity_score)

    class Meta(SerieMeta):
        pass


class SerieItem(SerieBase):
    genres = fields.Method("build_genres")

    def build_genres(self, obj):
        return GenreBase.loads(obj.content.genres)


class SerieExtra(SerieItem):
    # Extra fields from join with 'recommended_application'
    reco_engine = fields.String(attribute="engine", default=None)
    reco_score = fields.Float(attribute="score", default=None)

# ----

class SerieAdditionalMeta:
    model = SerieAdditionalModel
    include_fk = True

class SerieAdditionalBase(SQLAlchemyAutoSchema):
    class Meta(SerieAdditionalMeta):
        pass