from src import ma

from src.model import MetaUserGameModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserGameMeta:
    model = MetaUserGameModel


class MetaUserGameBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserGameMeta):
        pass
