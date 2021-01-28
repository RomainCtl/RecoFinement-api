from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.session import object_session
from sqlalchemy import event

from src import db
from .event import EpisodeAddedEvent, EpisodeDeletedEvent, ChangedEvent

EpisodeAdditionalGenresModel = db.Table("episode_additional_genres",
                                        db.Column("episode_id", db.Integer, db.ForeignKey(
                                            "episode_additional.episode_id"), primary_key=True),
                                        db.Column("genre_id", db.Integer, db.ForeignKey(
                                            "genre.genre_id"), primary_key=True)
                                        )


class EpisodeModel(db.Model):
    """
    Episode Model for storing episode related details
    """
    __tablename__ = "episode"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    imdbid = db.Column(db.String(255))
    title = db.Column(db.String(512), index=True)
    year = db.Column(db.Integer)
    season_number = db.Column(db.Integer)
    episode_number = db.Column(db.Integer)
    serie_id = db.Column(db.Integer, db.ForeignKey("serie.content_id"))

    content = db.relationship(
        "ContentModel", backref=db.backref("episode", uselist=False))

    @hybrid_property
    def episode_id(self):
        return self.content_id


class EpisodeAdditionalModel(db.Model):
    """
    Episode Model for storing episode related details added by a user
    """
    __tablename__ = "episode_additional"

    episode_id = db.Column(db.Integer, index=True, primary_key=True)
    imdbid = db.Column(db.String(255))
    title = db.Column(db.String(512), index=True)
    year = db.Column(db.Integer)
    season_number = db.Column(db.Integer)
    episode_number = db.Column(db.Integer)
    serie_id = db.Column(db.Integer, db.ForeignKey(
        "serie_additional.serie_id"))

    genres = db.relationship(
        "GenreModel", secondary=EpisodeAdditionalGenresModel, lazy="dynamic")


@event.listens_for(EpisodeModel, 'after_insert')
def receive_after_insert(mapper, connection, target):
    "listen for the 'after_insert' event"
    connection.execute(EpisodeAddedEvent.insert(target))


@event.listens_for(EpisodeModel, 'after_delete')
def receive_after_delete(mapper, connection, target):
    "listen for the 'after_delete' event"
    event = EpisodeDeletedEvent(object_id=target.content_id)
    connection.execute(event.delete())


@event.listens_for(EpisodeModel, 'after_update')
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
            model_name=EpisodeModel.__tablename__,
            attribute_name=attr.key,
            new_value=str(hist.added[0])
        ))
