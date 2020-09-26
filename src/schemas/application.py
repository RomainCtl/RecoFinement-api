# Application Schemas
from src import ma

from src.model import Application


class ApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("app_id", "name", "category", "rating", "reviews", "size", "installs",
                  "price", "content_rating", "genres", "last_updated", "current_version", "android_version")
