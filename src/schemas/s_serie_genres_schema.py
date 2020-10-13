from src import ma
from src.model import SSerieGenresModel
from src.utils import SQLAlchemyAutoSchema


class SSerieGenresMeta:
    model = SSerieGenresModel


class SSerieGenresBase(SQLAlchemyAutoSchema):
    class Meta(SSerieGenresMeta):
        pass