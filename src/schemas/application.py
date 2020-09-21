# Application Schemas
from src import ma

from src.model import Application


class ApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("uid", "app_name", "category", "rating", "reviews", "installs", "size", "price", "content_rating", "last_updated", "minimum_version", "latest_version")
