# Book Schemas
from src import ma

from src.model import Book


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("isbn", "title", "author", "year_of_publication",
                  "publisher", "image_url_s", "image_url_m", "image_url_l")
