from sqlalchemy.dialects.postgresql import UUID
import uuid

from src import db

SimilarsTracksModel = db.Table("similars_track",
                               db.Column("track_id0", db.Integer, db.ForeignKey(
                                   "track.track_id"), primary_key=True),
                               db.Column("track_id1", db.Integer, db.ForeignKey(
                                   "track.track_id"), primary_key=True),
                               db.Column("similarity", db.Float)
                               )


class TrackModel(db.Model):
    """
    Track Model for storing track related details
    """
    __tablename__ = "track"

    track_id = db.Column(db.Integer, primary_key=True,
                         autoincrement=True, index=True)
    title = db.Column(db.String(255), index=True)
    year = db.Column(db.SmallInteger)
    artist_name = db.Column(db.String(255), index=True)
    release = db.Column(db.String(255))
    track_mmid = db.Column(db.String(45))
    recording_mbid = db.Column(UUID(as_uuid=True))
    language = db.Column(db.String(45))
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer, default=0)
    url = db.Column(db.Text)
    covert_art_url = db.Column(db.Text)

    # Loaded immediately after loading Track, but when querying multiple tracks, you will not get additional queries.
    similars = db.relationship("TrackModel", secondary=SimilarsTracksModel,
                               primaryjoin=track_id == SimilarsTracksModel.c.track_id0,
                               secondaryjoin=track_id == SimilarsTracksModel.c.track_id1,
                               lazy="subquery")