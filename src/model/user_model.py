from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import CheckConstraint
import uuid

from src import db, bcrypt


MetaUserBookModel = db.Table("meta_user_book",
                             db.Column("user_id", db.Integer, db.ForeignKey(
                                 "user.user_id"), primary_key=True),
                             db.Column("isbn", db.String(13), db.ForeignKey(
                                 "book.isbn"), primary_key=True),
                             db.Column("rating", db.Integer, default=None),
                             CheckConstraint("rating <= 5 and rating >= 0")
                             )

MetaUserGameModel = db.Table("meta_user_game",
                             db.Column("user_id", db.Integer, db.ForeignKey(
                                 "user.user_id"), primary_key=True),
                             db.Column("game_id", db.Integer, db.ForeignKey(
                                 "game.game_id"), primary_key=True),
                             db.Column("purchase", db.Boolean, default=False),
                             db.Column("hours", db.Float, default=0),
                             db.Column("rating", db.Integer, default=None),
                             CheckConstraint("rating <= 5 and rating >= 0")
                             )

MetaUserApplicationModel = db.Table("meta_user_application",
                                    db.Column("user_id", db.Integer, db.ForeignKey(
                                        "user.user_id"), primary_key=True),
                                    db.Column("app_id", db.Integer, db.ForeignKey(
                                        "application.app_id"), primary_key=True),
                                    db.Column("review", db.Text, default=None),
                                    db.Column("popularity", db.Float,
                                              default=None),
                                    db.Column("subjectivity",
                                              db.Float, default=None),
                                    db.Column("rating", db.Integer,
                                              default=None),
                                    CheckConstraint(
                                        "rating <= 5 and rating >= 0")
                                    )

MetaUserMovieModel = db.Table("meta_user_movie",
                              db.Column("user_id", db.Integer, db.ForeignKey(
                                  "user.user_id"), primary_key=True),
                              db.Column("movie_id", db.Integer, db.ForeignKey(
                                  "movie.movie_id"), primary_key=True),
                              db.Column("rating", db.Integer, default=None),
                              CheckConstraint("rating <= 5 and rating >= 0")
                              )

MetaUserTrackModel = db.Table("meta_user_track",
                              db.Column("user_id", db.Integer, db.ForeignKey(
                                  "user.user_id"), primary_key=True),
                              db.Column("track_id", db.Integer, db.ForeignKey(
                                  "track.track_id"), primary_key=True),
                              db.Column("rating", db.Integer, default=None),
                              CheckConstraint("rating <= 5 and rating >= 0")
                              )

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
        "BookModel", secondary=MetaUserBookModel, lazy="subquery")
    meta_user_games = db.relationship(
        "GameModel", secondary=MetaUserGameModel, lazy="subquery")
    meta_user_applications = db.relationship(
        "ApplicationModel", secondary=MetaUserApplicationModel, lazy="subquery")
    meta_user_movies = db.relationship(
        "MovieModel", secondary=MetaUserMovieModel, lazy="subquery")
    meta_user_tracks = db.relationship(
        "TrackModel", secondary=MetaUserTrackModel, lazy="subquery")

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
