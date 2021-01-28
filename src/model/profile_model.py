from sqlalchemy import CheckConstraint
import uuid

from src import db, bcrypt
from src.utils import GUID

class MetaProfileContentModel(db.Model):
    """
    MetaProfileContent Model for storing metadata between profile and content
    """
    __tablename__ = "meta_profile_content"

    profile_id = db.Column(db.Integer, db.ForeignKey(
        "profile.profile_id", ondelete="CASCADE"), primary_key=True)
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


""" GroupMembersProfileModel = db.Table("group_members_profile",
                             db.Column("profile_id", db.Integer, db.ForeignKey(
                                 "profile.profile_id", ondelete="CASCADE"), primary_key=True),
                             db.Column("group_id", db.Integer, db.ForeignKey(
                                 "group_profile.group_id", ondelete="CASCADE"), primary_key=True)
                             ) """

LikedGenreProfileModel = db.Table("liked_genres_profile",
                           db.Column("profile_id", db.Integer, db.ForeignKey(
                               "profile.profile_id", ondelete="CASCADE"), primary_key=True),
                           db.Column("genre_id", db.Integer, db.ForeignKey(
                               "genre.genre_id", ondelete="CASCADE"), primary_key=True)
                           )


class RecommendedContentProfileModel(db.Model):
    """
    RecommendedContent Model for storing recommended contents for a profile
    """
    __tablename__ = "recommended_content_profile"

    profile_id = db.Column(db.Integer, db.ForeignKey(
        "profile.profile_id", ondelete="CASCADE"), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey(
        "content.content_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)
    engine_priority = db.Column(db.Integer)


class BadRecommendationContentProfileModel(db.Model):
    """
    BadRecommendationContent Model for storing bad recommended contents for a profile
    """
    __tablename__ = "bad_recommendation_content_profile"

    profile_id = db.Column(db.Integer, db.ForeignKey(
        "profile.profile_id", ondelete="CASCADE"), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey(
        "content.content_id", ondelete="CASCADE"), primary_key=True)
    reason_categorie = db.Column(db.Text, primary_key=True)
    reason = db.Column(db.Text, primary_key=True)


class ProfileModel(db.Model):
    """
    Profile Model for storing profile related details
    """
    __tablename__ = "profile"

    profile_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, index=True)
    uuid = db.Column(GUID(), default=uuid.uuid4, unique=True)
    profilename = db.Column(db.String(45), nullable=False)
    #uuid_user = db.Column(GUID(), db.ForeignKey("user.uuid", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)

    # Loaded immediately after loading Profile, but when querying multiple profiles, you will not get additional queries.
    meta_profile_contents = db.relationship(
        "MetaProfileContentModel", lazy="subquery")

    recommended_contents = db.relationship(
        "RecommendedContentProfileModel", lazy="subquery")

    bad_recommadation_contents = db.relationship(
        "BadRecommendationContentProfileModel", lazy="subquery")

    """ groups = db.relationship(
        "GroupProfileModel", secondary=GroupMembersProfileModel, lazy="dynamic", backref=db.backref('members', lazy='dynamic'))
    owned_groups = db.relationship(
        "GroupProfileModel", backref="owner", lazy='dynamic')

    linked_services = db.relationship(
        "ExternalModel", backref="profile", lazy='dynamic') """

    liked_genres = db.relationship(
        "GenreModel", secondary=LikedGenreProfileModel, lazy="dynamic")

    def __repr__(self):
        return f"<Profile {self.profilename}>"
