# Track Schemas
from src import ma
from src.model import TrackGenresModel
from src.utils import SQLAlchemyAutoSchema


class TrackGenresMeta:
    model = TrackGenresModel


class TrackGenresBase(SQLAlchemyAutoSchema):
    class Meta(TrackGenresMeta):
        pass
