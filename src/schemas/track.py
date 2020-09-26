# Track Schemas
from src import ma

from src.model import Track


class TrackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("track_id", "title", "year", "artist_name", "release", "recording_mbid",
                  "language", "rating", "rating_count", "url", "covert_art_url", "tags", "similars")
