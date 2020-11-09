from src import ma

from src.model import MetaUserBookModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserBookMeta:
    model = MetaUserBookModel


class MetaUserBookBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserBookMeta):
        fields = ["purchase", "rating", "review_see_count"]


class MetaUserBookItem(SQLAlchemyAutoSchema):
    class Meta(MetaUserBookMeta):
        fields = ["isbn", "purchase", "rating", "review_see_count"]
