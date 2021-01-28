from src import db
from .event import Event, ChangedEvent, DeletionEvent


class EpisodeAddedEvent(Event, db.Model):
    __tablename__ = "episode_added_event"

    imdbid = db.Column(db.String(255))
    title = db.Column(db.String(512))
    year = db.Column(db.Integer)
    season_number = db.Column(db.Integer)
    episode_number = db.Column(db.Integer)
    serie_id = db.Column(db.Integer)

    @classmethod
    def insert(cls, target):
        return cls.__table__.insert().values(
            object_id=target.content_id,
            imdbid=target.imdbid,
            title=target.title,
            year=target.year,
            season_number=target.season_number,
            episode_number=target.episode_number,
            serie_id=target.serie_id,
        )


class EpisodeDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="episode", **kwargs)
