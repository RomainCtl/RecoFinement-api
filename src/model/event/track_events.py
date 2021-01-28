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

    @classmethod
    def insert(cls, target):
        return cls.__table__.insert().values(
            object_id=target.content_id,
            title=target.title,
            year=target.year,
            artist_name=target.artist_name,
            release=target.release,
            track_mmid=target.track_mmid,
            recording_mbid=target.recording_mbid,
            spotify_id=target.spotify_id,
            covert_art_url=target.covert_art_url,
        )


class TrackDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="track", **kwargs)
