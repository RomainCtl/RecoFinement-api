from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..addons import db


trackTags = db.Table("track_tags",
    db.Column("track_id", db.Integer, db.ForeignKey("track.id"), primary_key=True),
    db.Column("tag", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
    db.Column("count", db.Integer, default=0)
)

class Track(db.Model):
    """
    Track Model for storing track related details
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(255), index=True)
    artist_name = db.Column(db.String(255), index=True)
    album_name = db.Column(db.String(255))
    language = db.Column(db.String(2))
    date_year = db.Column(db.SmallInteger)
    date_month = db.Column(db.SmallInteger)
    date_day = db.Column(db.SmallInteger)
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer, default=0)

    # Loaded immediately after loading Track, but when querying multiple tracks, you will not get additional queries.
    tags = db.relationship("Tag", secondary=trackTags, lazy="subquery")

