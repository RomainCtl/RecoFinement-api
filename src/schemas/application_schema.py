# Application Schemas
from src import ma
from src.model import ApplicationModel
from src.utils import SQLAlchemyAutoSchema


class ApplicationMeta:
    model = ApplicationModel


class ApplicationBase(SQLAlchemyAutoSchema):
    categorie = ma.Nested("GenreBase")

    class Meta(ApplicationMeta):
        pass
