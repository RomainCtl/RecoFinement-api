# External Schemas
from src import ma

from src.model import ExternalModel
from src.utils import SQLAlchemyAutoSchema

from src.utils import DTOSchema


class ExternalMeta:
    model = ExternalModel


class ExternalBase(SQLAlchemyAutoSchema):
    class Meta(ExternalMeta):
        fields = ("service_id", "service_name")
