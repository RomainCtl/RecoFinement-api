# Track Schemas
from src import ma

from src.model import Track


class TrackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("gid", "name", "artist_name", "album_name", "language", "date_year", "date_month", "date_day", "rating", "rating_count")
