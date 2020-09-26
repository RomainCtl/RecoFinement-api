# Game Schemas
from src import ma

from src.model import Game


class GameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("game_id", "steamid", "name", "short_description", "header_image", "website",
                  "developers", "publishers", "price", "genres", "recommendations", "release_date")
