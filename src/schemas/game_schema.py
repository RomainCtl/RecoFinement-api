# Game Schemas
from marshmallow import fields
from src import ma
from src.model import GameModel
from src.utils import SQLAlchemyAutoSchema


class GameMeta:
    model = GameModel


class GameBase(SQLAlchemyAutoSchema):
    class Meta(GameMeta):
        pass


class GameObject(SQLAlchemyAutoSchema):
    genres = ma.Nested("GenreBase", many=True)

    class Meta(GameMeta):
        pass


class GameExtra(GameObject):
    # Extra fields from join with 'recommended_application'
    reco_engine = fields.String(attribute="engine", default=None)
    reco_score = fields.Float(attribute="score", default=None)
