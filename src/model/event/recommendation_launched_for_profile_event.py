from datetime import datetime

from src import db
from ..content_model import ContentType


class RecoLaunchedLikedGenreModel(db.Model):
    """ Copy of interest for the recommendation history """
    __tablename__ = "recommendation_launched_liked_genre"

    event_id = db.Column(db.Integer, db.ForeignKey(
        "recommendation_launched_for_profile_event.id", ondelete="CASCADE"), primary_key=True)
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    content_type = db.Column(db.Enum(ContentType))


class RecoMetaModel(db.Model):
    """ Copy of meta for the recommendation history """
    __tablename__ = "recommendation_launched_meta"

    event_id = db.Column(db.Integer, db.ForeignKey(
        "recommendation_launched_for_profile_event.id", ondelete="CASCADE"), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey(
        "content.content_id", ondelete="CASCADE"), primary_key=True)
    rating = db.Column(db.Integer, default=None)
    last_rating_date = db.Column(db.DateTime, default=None)
    review_see_count = db.Column(db.Integer, default=0)
    last_review_see_date = db.Column(db.DateTime, default=None)
    count = db.Column(db.Integer, default=0)
    last_count_increment = db.Column(db.DateTime, default=None)


class RecoResultModel(db.Model):
    """ Result recommendation history for the event"""
    __tablename__ = "recommendation_launched_result"

    event_id = db.Column(db.Integer, db.ForeignKey(
        "recommendation_launched_for_profile_event.id", ondelete="CASCADE"), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey(
        "content.content_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)


class RecommendationLaunchedForProfileEvent(db.Model):
    """  """
    __tablename__ = "recommendation_launched_for_profile_event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    occured_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey(
        "profile.profile_id", ondelete="CASCADE"))

    liked_genres = db.relationship(
        "RecoLaunchedLikedGenreModel", lazy="subquery")

    meta = db.relationship(
        "RecoMetaModel", lazy="subquery")

    result = db.relationship(
        "RecoResultModel", lazy="subquery")

    profile = db.relationship(
        "ProfileModel", lazy="subquery")
