# Game Schemas
from marshmallow import fields
from src import ma
from src.model import GameModel, GameAdditionalModel
from src.utils import SQLAlchemyAutoSchema
from .genre_schema import GenreBase


class GameMeta:
    model = GameModel
    include_fk = True


class GameBase(SQLAlchemyAutoSchema):
    rating = fields.Function(lambda obj: obj.content.rating)
    rating_count = fields.Function(lambda obj: obj.content.rating_count)
    popularity_score = fields.Function(
        lambda obj: obj.content.popularity_score)

    game_id = ma.Function(lambda obj: obj.game_id)

    class Meta(GameMeta):
        pass


class GameObject(GameBase):
    genres = fields.Method("build_genres")

    def build_genres(self, obj):
        return GenreBase.loads(obj.content.genres)


class GameExtra(GameObject):
    # Extra fields from join with 'recommended_application'
    reco_engine = fields.String(attribute="engine", default=None)
    reco_score = fields.Float(attribute="score", default=None)

# ----

class GameAdditionalMeta:
    model = GameAdditionalModel
    include_fk = True

class GameAdditionalBase(SQLAlchemyAutoSchema):
    class Meta(GameAdditionalMeta):
        pass