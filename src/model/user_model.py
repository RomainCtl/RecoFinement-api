from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import CheckConstraint
import uuid

from src import db, bcrypt


class MetaUserBookModel(db.Model):
    """
    MetaUserBook Model for storing metadata between user and book
    """
    __tablename__ = "meta_user_book"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    isbn = db.Column(db.String(13), db.ForeignKey(
        "book.isbn", ondelete="CASCADE"), primary_key=True)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)
    purchase = db.Column(db.Boolean, default=False)
    review_see_count = db.Column(db.Integer, default=0)


class MetaUserGameModel(db.Model):
    """
    MetaUserGame Model for storing metadata between user and game
    """
    __tablename__ = "meta_user_game"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(
        "game.game_id", ondelete="CASCADE"), primary_key=True)
    purchase = db.Column(db.Boolean, default=False)
    hours = db.Column(db.Float, default=0)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)
    review_see_count = db.Column(db.Integer, default=0)


class MetaUserApplicationModel(db.Model):
    """
    MetaUserApplication Model for storing metadata between user and application
    """
    __tablename__ = "meta_user_application"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey(
        "application.app_id", ondelete="CASCADE"), primary_key=True)
    review = db.Column(db.Text, default=None)
    popularity = db.Column(db.Float, default=None)
    subjectivity = db.Column(db.Float, default=None)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)
    review_see_count = db.Column(db.Integer, default=0)
    downloaded = db.Column(db.Boolean, default=False)


class MetaUserMovieModel(db.Model):
    """
    MetaUserMovie Model for storing metadata between user and movie
    """
    __tablename__ = "meta_user_movie"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        "movie.movie_id", ondelete="CASCADE"), primary_key=True)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)
    watch_count = db.Column(db.Integer, default=0)
    review_see_count = db.Column(db.Integer, default=0)


class MetaUserTrackModel(db.Model):
    """
    MetaUserTrack Model for storing metadata between user and track
    """
    __tablename__ = "meta_user_track"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey(
        "track.track_id", ondelete="CASCADE"), primary_key=True)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)
    play_count = db.Column(db.Integer, default=0)
    review_see_count = db.Column(db.Integer, default=0)
    last_played_date = db.Column(db.DateTime, default=None)


class MetaUserSerieModel(db.Model):
    """
    MetaUserTrack Model for storing metadata between user and serie
    """
    __tablename__ = "meta_user_serie"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey(
        "serie.serie_id", ondelete="CASCADE"), primary_key=True)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)
    num_watched_episodes = db.Column(db.Integer, default=0)
    review_see_count = db.Column(db.Integer, default=0)


GroupMembersModel = db.Table("group_members",
                             db.Column("user_id", db.Integer, db.ForeignKey(
                                 "user.user_id", ondelete="CASCADE"), primary_key=True),
                             db.Column("group_id", db.Integer, db.ForeignKey(
                                 "group.group_id", ondelete="CASCADE"), primary_key=True)
                             )

LikedGenreModel = db.Table("liked_genres",
                           db.Column("user_id", db.Integer, db.ForeignKey(
                               "user.user_id", ondelete="CASCADE"), primary_key=True),
                           db.Column("genre_id", db.Integer, db.ForeignKey(
                               "genre.genre_id", ondelete="CASCADE"), primary_key=True)
                           )


class RecommendedApplicationModel(db.Model):
    """
    RecommendedApplication Model for storing recommended applications for a user
    """
    __tablename__ = "recomended_application"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey(
        "application.app_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)


class RecommendedBookModel(db.Model):
    """
    RecommendedBook Model for storing recommended books for a user
    """
    __tablename__ = "recomended_book"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    isbn = db.Column(db.String(13), db.ForeignKey(
        "book.isbn", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)


class RecommendedGameModel(db.Model):
    """
    RecommendedGame Model for storing recommended games for a user
    """
    __tablename__ = "recomended_game"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(
        "game.game_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)


class RecommendedMovieModel(db.Model):
    """
    RecommendedMovie Model for storing recommended movies for a user
    """
    __tablename__ = "recomended_movie"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        "movie.movie_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)


class RecommendedSerieModel(db.Model):
    """
    RecommendedSerie Model for storing recommended series for a user
    """
    __tablename__ = "recomended_serie"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey(
        "serie.serie_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)


class RecommendedTrackModel(db.Model):
    """
    RecommendedTrack Model for storing recommended tracks for a user
    """
    __tablename__ = "recomended_track"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey(
        "track.track_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)


class UserModel(db.Model):
    """
    User Model for storing user related details
    """
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, index=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(45), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    preferences_defined = db.Column(db.Boolean, default=False)

    # Loaded immediately after loading User, but when querying multiple users, you will not get additional queries.
    meta_user_books = db.relationship("MetaUserBookModel", lazy="subquery")
    meta_user_games = db.relationship("MetaUserGameModel", lazy="subquery")
    meta_user_applications = db.relationship(
        "MetaUserApplicationModel", lazy="subquery")
    meta_user_movies = db.relationship("MetaUserMovieModel", lazy="subquery")
    meta_user_tracks = db.relationship("MetaUserTrackModel", lazy="subquery")
    meta_user_series = db.relationship("MetaUserSerieModel", lazy="subquery")

    recommended_applications = db.relationship(
        "RecommendedApplicationModel", lazy="subquery")
    recommended_books = db.relationship(
        "RecommendedBookModel", lazy="subquery")
    recommended_games = db.relationship(
        "RecommendedGameModel", lazy="subquery")
    recommended_movies = db.relationship(
        "RecommendedMovieModel", lazy="subquery")
    recommended_series = db.relationship(
        "RecommendedSerieModel", lazy="subquery")
    recommended_tracks = db.relationship(
        "RecommendedTrackModel", lazy="subquery")

    groups = db.relationship(
        "GroupModel", secondary=GroupMembersModel, lazy="dynamic", backref=db.backref('members', lazy='dynamic'))
    owned_groups = db.relationship(
        "GroupModel", backref="owner", lazy='dynamic')

    linked_services = db.relationship(
        "ExternalModel", backref="user", lazy='dynamic')

    liked_genres = db.relationship(
        "GenreModel", secondary=LikedGenreModel, lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
