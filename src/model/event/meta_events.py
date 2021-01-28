from src import db
from .event import Event, ChangedEvent


class MetaAddedEvent(Event, db.Model):
    __tablename__ = "meta_added_event"

    rating = db.Column(db.Integer, default=None)
    review_see_count = db.Column(db.Integer, default=0)
    count = db.Column(db.Integer, default=0)


class MetaChangedRatingEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="meta", attribute_name="rating", **kwargs)


class MetaChangedReviewSeeCountEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="meta",
                         attribute_name="review_see_count", **kwargs)


class MetaChangedCountEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="meta", attribute_name="count", **kwargs)
