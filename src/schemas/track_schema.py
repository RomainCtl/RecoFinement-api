# Track Schemas
from src import ma
from src.model import TrackModel
from src.utils import SQLAlchemyAutoSchema


class TrackMeta:
    model = TrackModel


class TrackBase(SQLAlchemyAutoSchema):
    class Meta(TrackMeta):
        pass


class TrackObject(SQLAlchemyAutoSchema):
    genres = ma.Nested("TrackGenresBase", many=True)

    class Meta(TrackMeta):
        fields = ("track_id", "title", "year", "artist_name", "release", "track_mmid", "recording_mbid",
                  "language", "rating", "rating_count", "spotify_id", "covert_art_url", "genres")
