# Episode Schemas
from marshmallow import fields
from src import ma
from src.model import EpisodeModel, EpisodeAdditionalModel
from src.utils import SQLAlchemyAutoSchema


class EpisodeMeta:
    model = EpisodeModel
    include_fk = True


class EpisodeBase(SQLAlchemyAutoSchema):
    rating = fields.Function(lambda obj: obj.content.rating)
    rating_count = fields.Function(lambda obj: obj.content.rating_count)

    class Meta(EpisodeMeta):
        pass

# ----

class EpisodeAdditionalMeta:
    model = EpisodeAdditionalModel
    include_fk = True

class EpisodeAdditionalBase(SQLAlchemyAutoSchema):
    class Meta(EpisodeAdditionalMeta):
        pass