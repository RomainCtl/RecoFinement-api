# Track Schemas
from src import ma
from src.model import TrackModel
from src.utils import SQLAlchemyAutoSchema


class TrackMeta:
    model = TrackModel


class TrackBase(SQLAlchemyAutoSchema):
    class Meta(TrackMeta):
        pass
