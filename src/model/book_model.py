from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.session import object_session
from sqlalchemy import event

from src import db
from .event import BookAddedEvent, BookDeletedEvent, ChangedEvent


class BookModel(db.Model):
    """
    Book Model for storing book related details
    """
    __tablename__ = "book"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    isbn = db.Column(db.String(13), unique=True,
                     nullable=False, index=True)
    title = db.Column(db.String(255), index=True)
    author = db.Column(db.String(255), index=True)
    year_of_publication = db.Column(db.Integer)
    publisher = db.Column(db.String(255))
    image_url_s = db.Column(db.Text)
    image_url_m = db.Column(db.Text)
    image_url_l = db.Column(db.Text)

    content = db.relationship(
        "ContentModel", backref=db.backref("book", uselist=False))

    @hybrid_property
    def book_id(self):
        return self.content_id


@event.listens_for(BookModel, 'after_insert')
def receive_after_insert(mapper, connection, target):
    "listen for the 'after_insert' event"
    connection.execute(BookAddedEvent.insert(target))


@event.listens_for(BookModel, 'after_delete')
def receive_after_delete(mapper, connection, target):
    "listen for the 'after_delete' event"
    event = BookDeletedEvent(object_id=target.content_id)
    connection.execute(event.delete())


@event.listens_for(BookModel, 'after_update')
def receive_after_update(mapper, connection, target):
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
            model_name=BookModel.__tablename__,
            attribute_name=attr.key,
            new_value=str(hist.added[0])
        ))
