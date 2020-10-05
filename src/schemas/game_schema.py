# Game Schemas
from src import ma
from src.model import GameModel
from src.utils import SQLAlchemyAutoSchema


class GameMeta:
    model = GameModel


class GameBase(SQLAlchemyAutoSchema):
    class Meta(GameMeta):
        pass
