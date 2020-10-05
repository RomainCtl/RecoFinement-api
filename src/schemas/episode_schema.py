# Episode Schemas
from src import ma
from src.model import EpisodeModel
from src.utils import SQLAlchemyAutoSchema


class EpisodeMeta:
    model = EpisodeModel


class EpisodeBase(SQLAlchemyAutoSchema):
    class Meta(EpisodeMeta):
        pass
