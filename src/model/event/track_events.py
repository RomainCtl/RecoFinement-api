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


class TrackChangedTitleEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="track", attribute_name="title", **kwargs)


class TrackChangedYearEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="track", attribute_name="year", **kwargs)


class TrackChangedArtistNameEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="track", attribute_name="artist_name", **kwargs)


class TrackChangedReleaseEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="track", attribute_name="release", **kwargs)


class TrackChangedTrackMmidEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="track", attribute_name="track_mmid", **kwargs)


class TrackChangedRecordingMbidEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="track",
                         attribute_name="recording_mbid", **kwargs)


class TrackChangedSpotifyIdEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="track", attribute_name="spotify_id", **kwargs)


class TrackChangedCovertArtUrlEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="track",
                         attribute_name="covert_art_url", **kwargs)
