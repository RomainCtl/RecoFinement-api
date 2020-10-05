from src import ma

from src.model import MetaUserSerieModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserSerieMeta:
    model = MetaUserSerieModel


class MetaUserSerieBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserSerieMeta):
        pass
