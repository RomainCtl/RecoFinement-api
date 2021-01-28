# Application Schemas
from marshmallow import fields
from src import ma
from src.model import ApplicationModel, ApplicationAdditionalModel
from src.utils import SQLAlchemyAutoSchema


class ApplicationMeta:
    model = ApplicationModel
    include_fk = True


class ApplicationBase(SQLAlchemyAutoSchema):
    rating = fields.Function(lambda obj: obj.content.rating)
    rating_count = fields.Function(lambda obj: obj.content.rating_count)
    popularity_score = fields.Function(
        lambda obj: obj.content.popularity_score)

    categorie = ma.Nested("GenreBase")

    app_id = ma.Function(lambda obj: obj.app_id)

    class Meta(ApplicationMeta):
        pass


class ApplicationExtra(ApplicationBase):
    # Extra fields from join with 'recommended_application'
    reco_engine = fields.String(attribute="engine", default=None)
    reco_score = fields.Float(attribute="score", default=None)

# ----

class ApplicationAdditionalMeta:
    model = ApplicationAdditionalModel
    include_fk = True

class ApplicationAdditionalBase(SQLAlchemyAutoSchema):
    class Meta(ApplicationAdditionalMeta):
        pass
