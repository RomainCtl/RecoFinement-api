from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.session import object_session
from sqlalchemy import event

from src import db
from .event.application_events import ApplicationAddedEvent, ApplicationDeletedEvent, ChangedEvent


class ApplicationModel(db.Model):
    """
    Application Model for storing application related details
    """
    __tablename__ = "application"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True, index=True)
    size = db.Column(db.String(255))
    installs = db.Column(db.String(255))
    type = db.Column(db.String(45))
    price = db.Column(db.String(45))
    content_rating = db.Column(db.String(255))
    last_updated = db.Column(db.String(255))
    current_version = db.Column(db.String(255))
    android_version = db.Column(db.String(255))
    cover = db.Column(db.Text)

    content = db.relationship(
        "ContentModel", backref=db.backref("application", uselist=False))

    @hybrid_property
    def app_id(self):
        return self.content_id

    @hybrid_property
    def categorie(self):
        return self.content.genres[0] if self.content.genres else None


@event.listens_for(ApplicationModel, 'after_insert')
def receive_after_insert(mapper, connection, target):
    "listen for the 'after_insert' event"
    connection.execute(ApplicationAddedEvent.insert(target))


@event.listens_for(ApplicationModel, 'after_delete')
def receive_after_delete(mapper, connection, target):
    "listen for the 'after_delete' event"
    event = ApplicationDeletedEvent(object_id=target.content_id)
    connection.execute(event.delete())


@event.listens_for(ApplicationModel, 'after_update')
def receive_after_delete(mapper, connection, target):
    "listen for the 'after_update' event"
    if not object_session(target).is_modified(target, include_collections=False):
        return

    changes = {}
    for attr in db.inspect(target).attrs:
        hist = attr.load_history()

        if not hist.has_changes():
            continue

        # hist.deleted holds old value
        # hist.added holds new value
        connection.execute(ChangedEvent.__table__.insert().values(
            object_id=target.content_id,
            model_name=ApplicationModel.__tablename__,
            attribute_name=attr.key,
            new_value=hist.added
        ))
