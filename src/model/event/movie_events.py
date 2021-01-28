from src import db
from .event import Event, ChangedEvent, DeletionEvent


class MovieAddedEvent(Event, db.Model):
    __tablename__ = "movie_added_event"

    title = db.Column(db.String(255))
    language = db.Column(db.String(255))
    actors = db.Column(db.Text)
    year = db.Column(db.String(255))
    producers = db.Column(db.Text)
    director = db.Column(db.Text)
    writer = db.Column(db.Text)
    imdbid = db.Column(db.String(255))
    tmdbid = db.Column(db.String(255))
    cover = db.Column(db.Text)
    plot_outline = db.Column(db.Text)

    @classmethod
    def insert(cls, target):
        return cls.__table__.insert().values(
            object_id=target.content_id,
            title=target.title,
            language=target.language,
            actors=target.actors,
            year=target.year,
            producers=target.producers,
            director=target.director,
            writer=target.writer,
            imdbid=target.imdbid,
            tmdbid=target.tmdbid,
            cover=target.cover,
            plot_outline=target.plot_outline,
        )


class MovieDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", **kwargs)
