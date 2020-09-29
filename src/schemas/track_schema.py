# Track Schemas
from src import ma
from src.model import TrackModel


class TrackMeta:
    model = TrackModel


class TrackBase(ma.SQLAlchemyAutoSchema):
    class Meta(TrackMeta):
        pass
