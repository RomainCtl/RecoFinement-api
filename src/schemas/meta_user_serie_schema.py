from src import ma

from src.model import MetaUserSerieModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserSerieMeta:
    model = MetaUserSerieModel


class MetaUserSerieBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserSerieMeta):
        fields = ["rating", "num_watched_episodes", "review_see_count"]


class MetaUserSerieItem(SQLAlchemyAutoSchema):
    class Meta(MetaUserSerieMeta):
        fields = ["serie_id", "rating",
                  "num_watched_episodes", "review_see_count"]
