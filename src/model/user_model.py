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
        "user.user_id"), primary_key=True)
    isbn = db.Column(db.String(13), db.ForeignKey(
        "book.isbn"), primary_key=True)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)


class MetaUserGameModel(db.Model):
    """
    MetaUserGame Model for storing metadata between user and game
    """
    __tablename__ = "meta_user_game"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(
        "game.game_id"), primary_key=True)
    purchase = db.Column(db.Boolean, default=False)
    hours = db.Column(db.Float, default=0)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)


class MetaUserApplicationModel(db.Model):
    """
    MetaUserApplication Model for storing metadata between user and application
    """
    __tablename__ = "meta_user_application"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey(
        "application.app_id"), primary_key=True)
    review = db.Column(db.Text, default=None)
    popularity = db.Column(db.Float, default=None)
    subjectivity = db.Column(db.Float, default=None)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)


class MetaUserMovieModel(db.Model):
    """
    MetaUserMovie Model for storing metadata between user and movie
    """
    __tablename__ = "meta_user_movie"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        "movie.movie_id"), primary_key=True)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)


class MetaUserTrackModel(db.Model):
    """
    MetaUserTrack Model for storing metadata between user and track
    """
    __tablename__ = "meta_user_track"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey(
        "track.track_id"), primary_key=True)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)


GroupMembersModel = db.Table("group_members",
                             db.Column("user_id", db.Integer, db.ForeignKey(
                                 "user.user_id"), primary_key=True),
                             db.Column("group_id", db.Integer, db.ForeignKey(
                                 "group.group_id"), primary_key=True)
                             )


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

    # Loaded immediately after loading Track, but when querying multiple tracks, you will not get additional queries.
    meta_user_books = db.relationship(
        "BookModel", secondary=MetaUserBookModel.__table__, lazy="subquery")
    meta_user_games = db.relationship(
        "GameModel", secondary=MetaUserGameModel.__table__, lazy="subquery")
    meta_user_applications = db.relationship(
        "ApplicationModel", secondary=MetaUserApplicationModel.__table__, lazy="subquery")
    meta_user_movies = db.relationship(
        "MovieModel", secondary=MetaUserMovieModel.__table__, lazy="subquery")
    meta_user_tracks = db.relationship(
        "TrackModel", secondary=MetaUserTrackModel.__table__, lazy="subquery")

    groups = db.relationship(
        "GroupModel", secondary=GroupMembersModel, lazy="dynamic", backref=db.backref('members', lazy='dynamic'))
    owned_groups = db.relationship(
        "GroupModel", backref="owner", lazy='dynamic')

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
