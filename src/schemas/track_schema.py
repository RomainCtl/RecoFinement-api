# Track Schemas
from marshmallow import fields
from src import ma
from src.model import TrackModel
from src.utils import SQLAlchemyAutoSchema


class TrackMeta:
    model = TrackModel


class TrackBase(SQLAlchemyAutoSchema):
    class Meta(TrackMeta):
        pass


class TrackObject(SQLAlchemyAutoSchema):
    genres = ma.Nested("GenreBase", many=True)

    class Meta(TrackMeta):
        fields = ("track_id", "title", "year", "artist_name", "release", "track_mmid",
                  "recording_mbid", "rating", "rating_count", "spotify_id", "covert_art_url", "genres")


class TrackExtra(TrackObject):
    # Extra fields from join with 'recommended_application'
    reco_engine = fields.String(attribute="engine", default=None)
    reco_score = fields.Float(attribute="score", default=None)
