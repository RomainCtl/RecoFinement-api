from src import ma

from src.model import MetaUserMovieModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserMovieMeta:
    model = MetaUserMovieModel


class MetaUserMovieBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserMovieMeta):
        fields = ["rating", "watch_count", "review_see_count"]


class MetaUserMovieItem(SQLAlchemyAutoSchema):
    class Meta(MetaUserMovieMeta):
        fields = ["movie_id", "rating", "watch_count", "review_see_count"]
