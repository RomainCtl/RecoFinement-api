# Serie Schemas
from marshmallow import fields
from src import ma
from src.model import SerieModel
from src.utils import SQLAlchemyAutoSchema


class SerieMeta:
    model = SerieModel


class SerieBase(SQLAlchemyAutoSchema):
    class Meta(SerieMeta):
        pass


class SerieItem(SQLAlchemyAutoSchema):
    genres = ma.Nested("GenreBase", many=True)

    class Meta(SerieMeta):
        pass


class SerieExtra(SerieItem):
    # Extra fields from join with 'recommended_application'
    reco_engine = fields.String(attribute="engine", default=None)
    reco_score = fields.Float(attribute="score", default=None)
