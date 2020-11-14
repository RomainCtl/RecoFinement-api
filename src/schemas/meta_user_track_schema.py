from src import ma

from src.model import MetaUserTrackModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserTrackMeta:
    model = MetaUserTrackModel


class MetaUserTrackBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserTrackMeta):
        fields = ["rating", "play_count",
                  "last_played_date", "review_see_count"]


class MetaUserTrackItem(SQLAlchemyAutoSchema):
    class Meta(MetaUserTrackMeta):
        fields = ["track_id", "rating", "play_count",
                  "last_played_date", "review_see_count"]
