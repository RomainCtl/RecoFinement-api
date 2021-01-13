from sqlalchemy import CheckConstraint
import uuid

from src import db, bcrypt
from src.utils import GUID


UserRoleModel = db.Table("user_role",
                         db.Column("user_id", db.Integer, db.ForeignKey(
                             "user.user_id", ondelete="CASCADE"), primary_key=True),
                         db.Column("role_id", db.Integer, db.ForeignKey(
                             "role.role_id"), primary_key=True)
                         )


class MetaUserContentModel(db.Model):
    """
    MetaUserContent Model for storing metadata between user and content
    """
    __tablename__ = "meta_user_content"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey(
        "content.content_id", ondelete="CASCADE"), primary_key=True)
    rating = db.Column(db.Integer, CheckConstraint(
        "rating <= 5 and rating >= 0"), default=None)
    last_rating_date = db.Column(db.DateTime, default=None)
    review_see_count = db.Column(db.Integer, default=0)
    last_review_see_date = db.Column(db.DateTime, default=None)
    # can be play_count, watch_count, num_watched_episodes
    count = db.Column(db.Integer, default=0)
    last_count_increment = db.Column(db.DateTime, default=None)


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


class RecommendedContentModel(db.Model):
    """
    RecommendedContent Model for storing recommended contents for a user
    """
    __tablename__ = "recommended_content"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey(
        "content.content_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)
    engine_priority = db.Column(db.Integer)


class BadRecommendationContentModel(db.Model):
    """
    BadRecommendationContent Model for storing bad recommended contents for a user
    """
    __tablename__ = "bad_recommendation_content"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey(
        "content.content_id", ondelete="CASCADE"), primary_key=True)
    reason_categorie = db.Column(db.Text, primary_key=True)
    reason = db.Column(db.Text, primary_key=True)


class UserModel(db.Model):
    """
    User Model for storing user related details
    """
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, index=True)
    uuid = db.Column(GUID(), default=uuid.uuid4, unique=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(45), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    preferences_defined = db.Column(db.Boolean, default=False)

    # Loaded immediately after loading User, but when querying multiple users, you will not get additional queries.
    meta_user_contents = db.relationship(
        "MetaUserContentModel", lazy="subquery")

    recommended_contents = db.relationship(
        "RecommendedContentModel", lazy="subquery")

    bad_recommadation_contents = db.relationship(
        "BadRecommendationContentModel", lazy="subquery")

    groups = db.relationship(
        "GroupModel", secondary=GroupMembersModel, lazy="dynamic", backref=db.backref('members', lazy='dynamic'))
    owned_groups = db.relationship(
        "GroupModel", backref="owner", lazy='dynamic')

    linked_services = db.relationship(
        "ExternalModel", backref="user", lazy='dynamic')

    liked_genres = db.relationship(
        "GenreModel", secondary=LikedGenreModel, lazy="dynamic")

    role = db.relationship(
        "RoleModel", secondary=UserRoleModel, lazy="subquery")

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
