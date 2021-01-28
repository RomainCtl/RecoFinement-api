from src import db
from .event import Event, ChangedEvent, DeletionEvent


class BookAddedEvent(Event, db.Model):
    __tablename__ = "book_added_event"

    isbn = db.Column(db.String(13))
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    year_of_publication = db.Column(db.Integer)
    publisher = db.Column(db.String(255))
    image_url_s = db.Column(db.Text)
    image_url_m = db.Column(db.Text)
    image_url_l = db.Column(db.Text)


class BookDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="book", **kwargs)
