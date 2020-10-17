# Serie Schemas
from src import ma
from src.model import SerieModel
from src.utils import SQLAlchemyAutoSchema


class SerieMeta:
    model = SerieModel


class SerieBase(SQLAlchemyAutoSchema):
    class Meta(SerieMeta):
        pass


class SerieItem(SQLAlchemyAutoSchema):
    genres = ma.Nested("GenreBase", many=True)

    class Meta(SerieMeta):
        pass


class SerieObject(SQLAlchemyAutoSchema):
    episodes = ma.Nested("EpisodeBase", many=True)
    genres = ma.Nested("GenreBase", many=True)

    class Meta(SerieMeta):
        pass
