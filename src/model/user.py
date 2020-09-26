from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import CheckConstraint
import uuid

from src import db, bcrypt


MetaUserBook = db.Table("meta_user_book",
                        db.Column("user_id", db.Integer, db.ForeignKey(
                            "user.user_id"), primary_key=True),
                        db.Column("isbn", db.Integer, db.ForeignKey(
                            "book.isbn"), primary_key=True),
                        db.Column("rating", db.Integer, default=None),
                        CheckConstraint("rating <= 5 and rating >= 0")
                        )

MetaUserGame = db.Table("meta_user_game",
                        db.Column("user_id", db.Integer, db.ForeignKey(
                            "user.user_id"), primary_key=True),
                        db.Column("game_id", db.Integer, db.ForeignKey(
                            "game.game_id"), primary_key=True),
                        db.Column("purchase", db.Boolean, default=False),
                        db.Column("hours", db.Float, default=0),
                        db.Column("rating", db.Integer, default=None),
                        CheckConstraint("rating <= 5 and rating >= 0")
                        )

MetaUserApplication = db.Table("meta_user_application",
                               db.Column("user_id", db.Integer, db.ForeignKey(
                                   "user.user_id"), primary_key=True),
                               db.Column("app_id", db.Integer, db.ForeignKey(
                                   "application.app_id"), primary_key=True),
                               db.Column("review", db.Text, default=None),
                               db.Column("popularity", db.Float, default=None),
                               db.Column("subjectivity",
                                         db.Float, default=None),
                               db.Column("rating", db.Integer, default=None),
                               CheckConstraint("rating <= 5 and rating >= 0")
                               )

MetaUserTrack = db.Table("meta_user_track",
                         db.Column("user_id", db.Integer, db.ForeignKey(
                             "user.user_id"), primary_key=True),
                         db.Column("track_id", db.Integer, db.ForeignKey(
                             "track.track_id"), primary_key=True),
                         db.Column("play_count", db.Integer, default=0),
                         db.Column("rating", db.Integer, default=None),
                         CheckConstraint("rating <= 5 and rating >= 0")
                         )


class User(db.Model):
    """
    User Model for storing user related details
    """
    user_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, index=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(45), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Loaded immediately after loading Track, but when querying multiple tracks, you will not get additional queries.
    meta_user_books = db.relationship(
        "Book", secondary=MetaUserBook, lazy="subquery")
    meta_user_games = db.relationship(
        "Game", secondary=MetaUserGame, lazy="subquery")
    meta_user_applications = db.relationship(
        "Application", secondary=MetaUserApplication, lazy="subquery")
    meta_user_tracks = db.relationship(
        "Track", secondary=MetaUserTrack, lazy="subquery")

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
