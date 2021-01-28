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


class EpisodeDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="episode", **kwargs)
