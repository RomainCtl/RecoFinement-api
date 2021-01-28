from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.session import object_session
from sqlalchemy import event

from src import db
from .event import SerieAddedEvent, SerieDeletedEvent, ChangedEvent


class SerieModel(db.Model):
    """
    Serie Model for storing serie related details
    """
    __tablename__ = "serie"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    imdbid = db.Column(db.String(255))
    title = db.Column(db.String(255), index=True)
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    writers = db.Column(db.Text)
    directors = db.Column(db.Text)
    actors = db.Column(db.Text)
    cover = db.Column(db.Text)
    plot_outline = db.Column(db.Text)

    episodes = db.relationship(
        "EpisodeModel", backref="serie",  lazy="dynamic")

    content = db.relationship(
        "ContentModel", backref=db.backref("serie", uselist=False))

    @hybrid_property
    def serie_id(self):
        return self.content_id


@event.listens_for(SerieModel, 'after_insert')
def receive_after_insert(mapper, connection, target):
    "listen for the 'after_insert' event"
    connection.execute(SerieAddedEvent.insert(target))


@event.listens_for(SerieModel, 'after_delete')
def receive_after_delete(mapper, connection, target):
    "listen for the 'after_delete' event"
    event = SerieDeletedEvent(object_id=target.content_id)
    connection.execute(event.delete())


@event.listens_for(SerieModel, 'after_update')
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
            model_name=SerieModel.__tablename__,
            attribute_name=attr.key,
            new_value=str(hist.added[0])
        ))
