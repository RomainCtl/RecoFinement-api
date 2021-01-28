from src import db
from src.utils import GUID
from .event import Event, ChangedEvent, DeletionEvent


class TrackAddedEvent(Event, db.Model):
    __tablename__ = "track_added_event"

    title = db.Column(db.String(255))
    year = db.Column(db.SmallInteger)
    artist_name = db.Column(db.String(255))
    release = db.Column(db.String(255))
    track_mmid = db.Column(db.String(45))
    recording_mbid = db.Column(GUID())
    spotify_id = db.Column(db.String(45))
    covert_art_url = db.Column(db.Text)


class TrackDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="track", **kwargs)
