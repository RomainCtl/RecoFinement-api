from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.session import object_session
from sqlalchemy import event

from src import db
from .event import MovieAddedEvent, MovieDeletedEvent, ChangedEvent


class MovieModel(db.Model):
    """
    Movie Model for storing movie related details
    """
    __tablename__ = "movie"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    title = db.Column(db.String(255), index=True)
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

    content = db.relationship(
        "ContentModel", backref=db.backref("movie", uselist=False))

    @hybrid_property
    def movie_id(self):
        return self.content_id


@event.listens_for(MovieModel, 'after_insert')
def receive_after_insert(mapper, connection, target):
    "listen for the 'after_insert' event"
    connection.execute(MovieAddedEvent.insert(target))


@event.listens_for(MovieModel, 'after_delete')
def receive_after_delete(mapper, connection, target):
    "listen for the 'after_delete' event"
    event = MovieDeletedEvent(object_id=target.content_id)
    connection.execute(event.delete())


@event.listens_for(MovieModel, 'after_update')
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
            model_name=MovieModel.__tablename__,
            attribute_name=attr.key,
            new_value=str(hist.added[0])
        ))
