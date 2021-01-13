from src import ma

from src.model import MetaUserContentModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserContentMeta:
    model = MetaUserContentModel


class MetaUserContentBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserContentMeta):
        fields = ("rating", "last_rating_date",
                  "review_see_count", "last_review_see_date", "count", "last_count_increment")


class MetaUserContentItem(SQLAlchemyAutoSchema):
    class Meta(MetaUserContentMeta):
        fields = ("content_id", "rating", "last_rating_date",
                  "review_see_count", "last_review_see_date", "count", "last_count_increment")
