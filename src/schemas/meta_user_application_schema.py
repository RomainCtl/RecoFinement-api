from src import ma

from src.model import MetaUserApplicationModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserApplicationMeta:
    model = MetaUserApplicationModel


class MetaUserApplicationBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserApplicationMeta):
        pass
