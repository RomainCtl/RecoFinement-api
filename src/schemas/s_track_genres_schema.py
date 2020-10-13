from src import ma
from src.model import STrackGenresModel
from src.utils import SQLAlchemyAutoSchema


class STrackGenresMeta:
    model = STrackGenresModel


class STrackGenresBase(SQLAlchemyAutoSchema):
    class Meta(STrackGenresMeta):
        pass
