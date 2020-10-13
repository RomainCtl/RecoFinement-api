from src import ma
from src.model import SApplicationCategoriesModel
from src.utils import SQLAlchemyAutoSchema


class SApplicationCategoriesMeta:
    model = SApplicationCategoriesModel


class SApplicationCategoriesBase(SQLAlchemyAutoSchema):
    class Meta(SApplicationCategoriesMeta):
        pass