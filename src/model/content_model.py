from src import db
import enum

ContentGenresModel = db.Table("content_genres",
                              db.Column("content_id", db.Integer, db.ForeignKey(
                                  "content.content_id"), primary_key=True),
                              db.Column("genre_id", db.Integer, db.ForeignKey(
                                  "genre.genre_id"), primary_key=True)
                              )


class ContentType(enum.Enum):
    APPLICATION = "application"
    BOOK = "book"
    GAME = "game"
    MOVIE = "movie"
    SERIE = "serie"
    TRACK = "track"

    def __str__(self):
        return self.value


class SimilarsContentModel(db.Model):
    """
    SimilarsContent Model for storing similars content
    """
    __tablename__ = "similars_content"

    content_id0 = db.Column(db.Integer, db.ForeignKey(
        "content.content_id"), primary_key=True)
    content_id1 = db.Column(db.Integer, db.ForeignKey(
        "content.content_id"), primary_key=True)
    similarity = db.Column(db.Float)
    content_type0 = db.Column(db.Enum(ContentType))
    content_type1 = db.Column(db.Enum(ContentType))


class ContentModel(db.Model):
    """
    Content Model for storing content related details
    """
    __tablename__ = "content"

    content_id = db.Column(db.Integer, primary_key=True,
                           autoincrement=True, index=True)
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer, default=0)
    popularity_score = db.Column(db.Float, default=0)

    genres = db.relationship(
        "GenreModel", secondary=ContentGenresModel, lazy="subquery")

    similars = db.relationship("ContentModel", secondary=SimilarsContentModel.__table__,
                               primaryjoin=content_id == SimilarsContentModel.content_id0,
                               secondaryjoin=content_id == SimilarsContentModel.content_id1, lazy="subquery")
