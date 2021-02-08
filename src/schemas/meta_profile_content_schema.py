from src import ma

from src.model import MetaProfileContentModel
from src.utils import SQLAlchemyAutoSchema


class MetaProfileContentMeta:
    model = MetaProfileContentModel


class MetaProfileContentBase(SQLAlchemyAutoSchema):
    class Meta(MetaProfileContentMeta):
        fields = ("rating", "last_rating_date",
                  "review_see_count", "last_review_see_date", "count", "last_count_increment")


class MetaProfileApplicationItem(SQLAlchemyAutoSchema):
    application = ma.Nested("ApplicationBase")

    class Meta(MetaProfileContentMeta):
        fields = ("application", "rating", "last_rating_date",
                  "review_see_count", "last_review_see_date", "count", "last_count_increment")


class MetaProfileBookItem(SQLAlchemyAutoSchema):
    book = ma.Nested("BookBase")

    class Meta(MetaProfileContentMeta):
        fields = ("book", "rating", "last_rating_date",
                  "review_see_count", "last_review_see_date", "count", "last_count_increment")


class MetaProfileGameItem(SQLAlchemyAutoSchema):
    game = ma.Nested("GameBase")

    class Meta(MetaProfileContentMeta):
        fields = ("game", "rating", "last_rating_date",
                  "review_see_count", "last_review_see_date", "count", "last_count_increment")


class MetaProfileMovieItem(SQLAlchemyAutoSchema):
    movie = ma.Nested("MovieBase")

    class Meta(MetaProfileContentMeta):
        fields = ("movie", "rating", "last_rating_date",
                  "review_see_count", "last_review_see_date", "count", "last_count_increment")


class MetaProfileSerieItem(SQLAlchemyAutoSchema):
    serie = ma.Nested("SerieBase")

    class Meta(MetaProfileContentMeta):
        fields = ("serie", "rating", "last_rating_date",
                  "review_see_count", "last_review_see_date", "count", "last_count_increment")


class MetaProfileTrackItem(SQLAlchemyAutoSchema):
    track = ma.Nested("TrackBase")

    class Meta(MetaProfileContentMeta):
        fields = ("track", "rating", "last_rating_date",
                  "review_see_count", "last_review_see_date", "count", "last_count_increment")
