# Movie Schemas
from marshmallow import fields
from src import ma
from src.model import MovieModel
from src.utils import SQLAlchemyAutoSchema
from .genre_schema import GenreBase


class MovieMeta:
    model = MovieModel
    include_fk = True


class MovieBase(SQLAlchemyAutoSchema):
    rating = fields.Function(lambda obj: obj.content.rating)
    rating_count = fields.Function(lambda obj: obj.content.rating_count)
    popularity_score = fields.Function(
        lambda obj: obj.content.popularity_score)

    class Meta(MovieMeta):
        pass


class MovieObject(MovieBase):
    genres = fields.Method("build_genres")

    def build_genres(self, obj):
        return GenreBase.loads(obj.content.genres)


class MovieExtra(MovieObject):
    # Extra fields from join with 'recommended_application'
    reco_engine = fields.String(attribute="engine", default=None)
    reco_score = fields.Float(attribute="score", default=None)
