# Track Schemas
from marshmallow import fields
from src import ma
from src.model import TrackModel, TrackAdditionalModel
from src.utils import SQLAlchemyAutoSchema
from .genre_schema import GenreBase


class TrackMeta:
    model = TrackModel
    include_fk = True


class TrackBase(SQLAlchemyAutoSchema):
    rating = fields.Function(lambda obj: obj.content.rating)
    rating_count = fields.Function(lambda obj: obj.content.rating_count)
    popularity_score = fields.Function(
        lambda obj: obj.content.popularity_score)

    track_id = ma.Function(lambda obj: obj.track_id)

    class Meta(TrackMeta):
        pass


class TrackObject(TrackBase):
    genres = fields.Method("build_genres")

    def build_genres(self, obj):
        return GenreBase.loads(obj.content.genres)


class TrackExtra(TrackObject):
    # Extra fields from join with 'recommended_application'
    reco_engine = fields.String(attribute="engine", default=None)
    reco_score = fields.Float(attribute="score", default=None)

# ----

class TrackAdditionalMeta:
    model = TrackAdditionalModel
    include_fk = True

class TrackAdditionalBase(SQLAlchemyAutoSchema):
    class Meta(TrackAdditionalMeta):
        pass