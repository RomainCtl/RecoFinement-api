from src import ma

from src.model import MetaUserGameModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserGameMeta:
    model = MetaUserGameModel


class MetaUserGameBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserGameMeta):
        fields = ["purchase", "rating", "hours", "review_see_count"]


class MetaUserGameItem(SQLAlchemyAutoSchema):
    class Meta(MetaUserGameMeta):
        fields = ["game_id", "purchase", "rating", "hours", "review_see_count"]
