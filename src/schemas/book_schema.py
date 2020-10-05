# Book Schemas
from src import ma
from src.model import BookModel
from src.utils import SQLAlchemyAutoSchema


class BookMeta:
    model = BookModel


class BookBase(SQLAlchemyAutoSchema):
    class Meta(BookMeta):
        pass
