from src import db
from .event import Event, ChangedEvent


class MetaAddedEvent(Event, db.Model):
    __tablename__ = "meta_added_event"

    rating = db.Column(db.Integer, default=None)
    review_see_count = db.Column(db.Integer, default=0)
    count = db.Column(db.Integer, default=0)
