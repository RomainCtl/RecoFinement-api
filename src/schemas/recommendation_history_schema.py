# Application Schemas
from marshmallow import fields
from src import ma
from src.model import RecommendationLaunchedForProfileEvent, RecoLaunchedLikedGenreModel, RecoMetaModel, RecoResultModel
from src.utils import SQLAlchemyAutoSchema


class RecoLaunchedLikedGenreItem(SQLAlchemyAutoSchema):
    content_type = fields.Function(lambda obj: obj.content_type.value)

    class Meta:
        model = RecoLaunchedLikedGenreModel
        include_fk = True
        fields = ("name", "content_type")

# ---------------------------


class RecoMetaMeta:
    model = RecoMetaModel
    include_fk = True


class RecoMetaBase(SQLAlchemyAutoSchema):
    class Meta(RecoMetaMeta):
        fields = ("rating", "last_rating_date", "review_see_count",
                  "last_review_see_date", "count", "last_count_increment")


class RecoMetaApplicationItem(SQLAlchemyAutoSchema):
    application = ma.Nested("ApplicationBase")

    class Meta(RecoMetaMeta):
        fields = ("application", "rating", "last_rating_date", "review_see_count",
                  "last_review_see_date", "count", "last_count_increment")


class RecoMetaBookItem(SQLAlchemyAutoSchema):
    book = ma.Nested("BookBase")

    class Meta(RecoMetaMeta):
        fields = ("book", "rating", "last_rating_date", "review_see_count",
                  "last_review_see_date", "count", "last_count_increment")


class RecoMetaGameItem(SQLAlchemyAutoSchema):
    game = ma.Nested("GameBase")

    class Meta(RecoMetaMeta):
        fields = ("game", "rating", "last_rating_date", "review_see_count",
                  "last_review_see_date", "count", "last_count_increment")


class RecoMetaMovieItem(SQLAlchemyAutoSchema):
    movie = ma.Nested("MovieBase")

    class Meta(RecoMetaMeta):
        fields = ("movie", "rating", "last_rating_date", "review_see_count",
                  "last_review_see_date", "count", "last_count_increment")


class RecoMetaSerieItem(SQLAlchemyAutoSchema):
    serie = ma.Nested("SerieBase")

    class Meta(RecoMetaMeta):
        fields = ("serie", "rating", "last_rating_date", "review_see_count",
                  "last_review_see_date", "count", "last_count_increment")


class RecoMetaTrackItem(SQLAlchemyAutoSchema):
    track = ma.Nested("TrackBase")

    class Meta(RecoMetaMeta):
        fields = ("track", "rating", "last_rating_date", "review_see_count",
                  "last_review_see_date", "count", "last_count_increment")

# ---------------------------


class RecoResultMeta:
    model = RecoResultModel
    include_fk = True


class RecoResultBase(SQLAlchemyAutoSchema):
    class Meta(RecoResultMeta):
        fields = ("content_id", "score", "engine")


class RecoResultApplicationItem(SQLAlchemyAutoSchema):
    application = ma.Nested("ApplicationBase")

    class Meta(RecoResultMeta):
        fields = ("application", "score", "engine")


class RecoResultBookItem(SQLAlchemyAutoSchema):
    book = ma.Nested("BookBase")

    class Meta(RecoResultMeta):
        fields = ("book", "score", "engine")


class RecoResultGameItem(SQLAlchemyAutoSchema):
    game = ma.Nested("GameBase")

    class Meta(RecoResultMeta):
        fields = ("game", "score", "engine")


class RecoResultMovieItem(SQLAlchemyAutoSchema):
    movie = ma.Nested("MovieBase")

    class Meta(RecoResultMeta):
        fields = ("movie", "score", "engine")


class RecoResultSerieItem(SQLAlchemyAutoSchema):
    serie = ma.Nested("SerieBase")

    class Meta(RecoResultMeta):
        fields = ("serie", "score", "engine")


class RecoResultTrackItem(SQLAlchemyAutoSchema):
    track = ma.Nested("TrackBase")

    class Meta(RecoResultMeta):
        fields = ("track", "score", "engine")

# ---------------------------


class RecommendationLaunchedForProfileMeta:
    model = RecommendationLaunchedForProfileEvent
    include_fk = True


class RecommendationLaunchedForProfileBase(SQLAlchemyAutoSchema):
    profile = ma.Nested("ProfileBase")

    class Meta(RecommendationLaunchedForProfileMeta):
        fields = ("profile", "id", "occured_at")


class RecommendationLaunchedForProfileItem(SQLAlchemyAutoSchema):
    profile = ma.Nested("ProfileBase")
    liked_genres = ma.Nested("RecoLaunchedLikedGenreItem", many=True)

    class Meta(RecommendationLaunchedForProfileMeta):
        fields = ("profile", "liked_genres", "id", "occured_at")
