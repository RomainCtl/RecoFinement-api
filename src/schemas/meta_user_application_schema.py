from src import ma

from src.model import MetaUserApplicationModel
from src.utils import SQLAlchemyAutoSchema


class MetaUserApplicationMeta:
    model = MetaUserApplicationModel


class MetaUserApplicationBase(SQLAlchemyAutoSchema):
    class Meta(MetaUserApplicationMeta):
        fields = ["review", "rating", "downloaded", "review_see_count"]


class MetaUserApplicationItem(SQLAlchemyAutoSchema):
    class Meta(MetaUserApplicationMeta):
        fields = ["app_id", "review", "rating",
                  "downloaded", "review_see_count"]
