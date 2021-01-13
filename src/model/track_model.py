from sqlalchemy.ext.hybrid import hybrid_property

from src import db
from src.utils import GUID


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
