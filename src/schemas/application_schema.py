# Application Schemas
from marshmallow import fields
from src import ma
from src.model import ApplicationModel
from src.utils import SQLAlchemyAutoSchema


class ApplicationMeta:
    model = ApplicationModel


class ApplicationBase(SQLAlchemyAutoSchema):
    categorie = ma.Nested("GenreBase")

    class Meta(ApplicationMeta):
        pass


class ApplicationExtra(ApplicationBase):
    # Extra fields from join with 'recommended_application'
    reco_engine = fields.String(attribute="engine", default=None)
    reco_score = fields.Float(attribute="score", default=None)
