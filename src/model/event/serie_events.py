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

    @classmethod
    def insert(cls, target):
        return cls.__table__.insert().values(
            object_id=target.content_id,
            imdbid=target.imdbid,
            title=target.title,
            start_year=target.start_year,
            end_year=target.end_year,
            writers=target.writers,
            directors=target.directors,
            actors=target.actors,
            cover=target.cover,
            plot_outline=target.plot_outline,
        )


class SerieDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", **kwargs)
