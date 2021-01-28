from src import db
from .event import Event, ChangedEvent, DeletionEvent


class ApplicationAddedEvent(Event, db.Model):
    __tablename__ = "application_added_event"

    name = db.Column(db.String(255))
    size = db.Column(db.String(255))
    installs = db.Column(db.String(255))
    type = db.Column(db.String(45))
    price = db.Column(db.String(45))
    content_rating = db.Column(db.String(255))
    last_updated = db.Column(db.String(255))
    current_version = db.Column(db.String(255))
    android_version = db.Column(db.String(255))
    cover = db.Column(db.Text)

    @classmethod
    def insert(cls, target):
        return cls.__table__.insert().values(
            object_id=target.content_id,
            name=target.name,
            size=target.size,
            installs=target.installs,
            type=target.type,
            price=target.price,
            content_rating=target.content_rating,
            last_updated=target.last_updated,
            current_version=target.current_version,
            android_version=target.android_version,
            cover=target.cover,
        )


class ApplicationDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application", **kwargs)
