from src import db
from .event import Event, ChangedEvent


class MetaAddedEvent(Event, db.Model):
    __tablename__ = "meta_added_event"

    rating = db.Column(db.Integer, default=None)
    review_see_count = db.Column(db.Integer, default=0)
    count = db.Column(db.Integer, default=0)

    @classmethod
    def insert(cls, target):
        return cls.__table__.insert().values(
            object_id=target.content_id,
            rating=target.rating,
            review_see_count=target.review_see_count,
            count=target.count,
        )
