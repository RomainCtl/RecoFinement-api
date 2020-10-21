from src import ma

from src.model import MetaUserBookModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserBookMeta:
    model = MetaUserBookModel


class MetaUserBookBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserBookMeta):
        fields = ["purchase", "rating"]
