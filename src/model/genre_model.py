from src import db
import enum


class ContentType(enum.Enum):
    APPLICATION = "application"
    BOOK = "book"
    GAME = "game"
    MOVIE = "movie"
    SERIE = "serie"
    TRACK = "track"

    def __str__(self):
        return self.value


class LinkedGenreModel(db.Model):
    """
    LinkedGenreModel Model for storing similars track
    """
    __tablename__ = "linked_genre"

    genre_id0 = db.Column(db.Integer, db.ForeignKey(
        "genre.genre_id"), primary_key=True)
    genre_id1 = db.Column(db.Integer, db.ForeignKey(
        "genre.genre_id"), primary_key=True)
    ratio = db.Column(db.Float)


class GenreModel(db.Model):
    """
    Genre Model for storing group related details
    """
    __tablename__ = "genre"

    genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    count = db.Column(db.Integer)
    content_type = db.Column(db.Enum(ContentType))

    # Loaded immediately after loading Track, but when querying multiple tracks, you will not get additional queries.
    linked_genres = db.relationship("LinkedGenreModel", secondary=LinkedGenreModel.__table__,
                                    primaryjoin=genre_id == LinkedGenreModel.genre_id0,
                                    secondaryjoin=genre_id == LinkedGenreModel.genre_id1,
                                    lazy="dynamic")
