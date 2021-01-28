from src import db
from .event import Event, ChangedEvent, DeletionEvent


class GameAddedEvent(Event, db.Model):
    __tablename__ = "game_added_event"

    steamid = db.Column(db.Integer)
    name = db.Column(db.String(255))
    short_description = db.Column(db.Text)
    header_image = db.Column(db.String(255))
    website = db.Column(db.String(255))
    developers = db.Column(db.String(255))
    publishers = db.Column(db.String(255))
    price = db.Column(db.String(255))
    recommendations = db.Column(db.Integer)
    release_date = db.Column(db.String(255))


class GameDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game", **kwargs)
