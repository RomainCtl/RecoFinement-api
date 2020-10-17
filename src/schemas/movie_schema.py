# Movie Schemas
from src import ma
from src.model import MovieModel
from src.utils import SQLAlchemyAutoSchema


class MovieMeta:
    model = MovieModel


class MovieBase(SQLAlchemyAutoSchema):
    class Meta(MovieMeta):
        pass


class MovieObject(SQLAlchemyAutoSchema):
    genres = ma.Nested("GenreBase", many=True)

    class Meta(MovieMeta):
        pass
