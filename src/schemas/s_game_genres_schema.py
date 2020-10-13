from src import ma
from src.model import SGameGenresModel
from src.utils import SQLAlchemyAutoSchema


class SGameGenresMeta:
    model = SGameGenresModel


class SGameGenresBase(SQLAlchemyAutoSchema):
    class Meta(SGameGenresMeta):
        pass