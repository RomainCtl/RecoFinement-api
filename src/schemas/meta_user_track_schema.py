from src import ma

from src.model import MetaUserTrackModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserTrackMeta:
    model = MetaUserTrackModel


class MetaUserTrackBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserTrackMeta):
        fields = ["rating", "play_count"]
