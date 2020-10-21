from src import ma

from src.model import MetaUserMovieModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserMovieMeta:
    model = MetaUserMovieModel


class MetaUserMovieBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserMovieModel):
        fields = ["rating", "watch_count"]
