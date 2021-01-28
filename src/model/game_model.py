from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.session import object_session
from sqlalchemy import event

from src import db
from .event import GameAddedEvent, GameDeletedEvent, ChangedEvent


class GameModel(db.Model):
    """
    Game Model for storing game related details
    """
    __tablename__ = "game"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    steamid = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(255), index=True)
    short_description = db.Column(db.Text)
    header_image = db.Column(db.String(255))
    website = db.Column(db.String(255))
    developers = db.Column(db.String(255))
    publishers = db.Column(db.String(255))
    price = db.Column(db.String(255))
    recommendations = db.Column(db.Integer)
    release_date = db.Column(db.String(255))

    content = db.relationship(
        "ContentModel", backref=db.backref("game", uselist=False))

    @hybrid_property
    def game_id(self):
        return self.content_id


@event.listens_for(GameModel, 'after_insert')
def receive_after_insert(mapper, connection, target):
    "listen for the 'after_insert' event"
    connection.execute(GameAddedEvent.insert(target))


@event.listens_for(GameModel, 'after_delete')
def receive_after_delete(mapper, connection, target):
    "listen for the 'after_delete' event"
    event = GameDeletedEvent(object_id=target.content_id)
    connection.execute(event.delete())


@event.listens_for(GameModel, 'after_update')
def receive_after_update(mapper, connection, target):
    "listen for the 'after_update' event"
    if not object_session(target).is_modified(target, include_collections=False):
        return

    changes = {}
    for attr in db.inspect(target).attrs:
        hist = attr.load_history()

        if not hist.has_changes():
            continue

        # hist.deleted holds old value
        # hist.added holds new value
        connection.execute(ChangedEvent.__table__.insert().values(
            object_id=target.content_id,
            model_name=GameModel.__tablename__,
            attribute_name=attr.key,
            new_value=str(hist.added[0])
        ))
