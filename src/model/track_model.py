from sqlalchemy.ext.hybrid import hybrid_property

from src import db
from src.utils import GUID

TrackAdditionalGenresModel = db.Table("track_additional_genres",
                              db.Column("track_id", db.Integer, db.ForeignKey(
                                  "track_additional.track_id"), primary_key=True),
                              db.Column("genre_id", db.Integer, db.ForeignKey(
                                  "genre.genre_id"), primary_key=True)
                              )

class TrackModel(db.Model):
    """
    Track Model for storing track related details
    """
    __tablename__ = "track"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    title = db.Column(db.String(255), index=True)
    year = db.Column(db.SmallInteger)
    artist_name = db.Column(db.String(255), index=True)
    release = db.Column(db.String(255))
    track_mmid = db.Column(db.String(45))
    recording_mbid = db.Column(GUID())
    spotify_id = db.Column(db.String(45))
    covert_art_url = db.Column(db.Text)

    content = db.relationship(
        "ContentModel", backref=db.backref("track", uselist=False))

    @hybrid_property
    def track_id(self):
        return self.content_id


class TrackAdditionalModel(db.Model):
    """
    Track Model for storing track related details added by a user
    """
    __tablename__ = "track_additional"

    track_id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(255), index=True)
    year = db.Column(db.SmallInteger)
    artist_name = db.Column(db.String(255), index=True)
    release = db.Column(db.String(255))
    track_mmid = db.Column(db.String(45))
    recording_mbid = db.Column(GUID())
    spotify_id = db.Column(db.String(45))
    covert_art_url = db.Column(db.Text)

    genres = db.relationship(
        "GenreModel", secondary=TrackAdditionalGenresModel, lazy="dynamic")