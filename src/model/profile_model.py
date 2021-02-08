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


LikedGenreProfileModel = db.Table("liked_genres_profile",
                                  db.Column("profile_id", db.Integer, db.ForeignKey(
                                      "profile.profile_id", ondelete="CASCADE"), primary_key=True),
                                  db.Column("genre_id", db.Integer, db.ForeignKey(
                                      "genre.genre_id", ondelete="CASCADE"), primary_key=True)
                                  )


class ProfileModel(db.Model):
    """
    Profile Model for storing profile related details
    """
    __tablename__ = "profile"

    profile_id = db.Column(db.Integer, primary_key=True,
                           autoincrement=True, index=True)
    uuid = db.Column(GUID(), default=uuid.uuid4, unique=True)
    profilename = db.Column(db.String(45), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)

    # Loaded immediately after loading Profile, but when querying multiple profiles, you will not get additional queries.
    meta_profile_contents = db.relationship(
        "MetaProfileContentModel", lazy="subquery")

    liked_genres = db.relationship(
        "GenreModel", secondary=LikedGenreProfileModel, lazy="dynamic")

    def __repr__(self):
        return f"<Profile {self.profilename}>"
