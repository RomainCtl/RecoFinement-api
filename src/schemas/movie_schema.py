# Movie Schemas
from marshmallow import fields
from src import ma
from src.model import MovieModel
from src.utils import SQLAlchemyAutoSchema


class MovieMeta:
    model = MovieModel


class MovieBase(SQLAlchemyAutoSchema):
    class Meta(MovieMeta):
        pass


class MovieObject(SQLAlchemyAutoSchema):
    genres = ma.Nested("GenreBase", many=True)

    class Meta(MovieMeta):
        pass


class MovieExtra(MovieObject):
    # Extra fields from join with 'recommended_application'
    reco_engine = fields.String(attribute="engine", default=None)
    reco_score = fields.Float(attribute="score", default=None)
