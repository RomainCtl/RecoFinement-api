from src import ma

from src.model import MetaUserMovieModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserMovieMeta:
    model = MetaUserMovieModel


class MetaUserMovieBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserMovieModel):
        fields = ["rating", "watch_count", "review_see_count"]


class MetaUserMovieItem(SQLAlchemyAutoSchema):
    class Meta(MetaUserMovieModel):
        fields = ["movie_id", "rating", "watch_count", "review_see_count"]
