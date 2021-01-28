from src import db
from .event import Event, ChangedEvent, DeletionEvent


class SerieAddedEvent(Event, db.Model):
    __tablename__ = "serie_added_event"

    imdbid = db.Column(db.String(255))
    title = db.Column(db.String(255))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    writers = db.Column(db.Text)
    directors = db.Column(db.Text)
    actors = db.Column(db.Text)
    cover = db.Column(db.Text)
    plot_outline = db.Column(db.Text)


class SerieDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", **kwargs)
