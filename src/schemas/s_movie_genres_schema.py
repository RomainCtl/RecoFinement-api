from src import ma
from src.model import SMovieGenresModel
from src.utils import SQLAlchemyAutoSchema


class SMovieGenresMeta:
    model = SMovieGenresModel


class SMovieGenresBase(SQLAlchemyAutoSchema):
    class Meta(SMovieGenresMeta):
        pass
