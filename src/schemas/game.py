# Game Schemas
from src import ma

from src.model import Game


class GameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("uid", "name", "icon_url", "rating", "rating_count", "price", "in_app_purchases", "description", "developer", "languages", "size", "primary_genre", "genres", "original_release_date")
