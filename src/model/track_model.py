from src import db
from src.utils import GUID

TrackGenresModel = db.Table("track_genres",
                            db.Column("track_id", db.Integer, db.ForeignKey(
                                "track.track_id"), primary_key=True),
                            db.Column("genre_id", db.Integer, db.ForeignKey(
                                "genre.genre_id"), primary_key=True)
                            )


class SimilarsTracksModel(db.Model):
    """
    SimilarsTracks Model for storing similars track
    """
    __tablename__ = "similars_track"

    track_id0 = db.Column(db.Integer, db.ForeignKey(
        "track.track_id"), primary_key=True)
    track_id1 = db.Column(db.Integer, db.ForeignKey(
        "track.track_id"), primary_key=True)
    similarity = db.Column(db.Float)


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
    recording_mbid = db.Column(GUID())
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer, default=0)
    spotify_id = db.Column(db.String(45))
    covert_art_url = db.Column(db.Text)
    popularity_score = db.Column(db.Float, default=0)

    # Loaded immediately after loading Track, but when querying multiple tracks, you will not get additional queries.
    similars = db.relationship("TrackModel", secondary=SimilarsTracksModel.__table__,
                               primaryjoin=track_id == SimilarsTracksModel.track_id0,
                               secondaryjoin=track_id == SimilarsTracksModel.track_id1,
                               lazy="subquery")

    genres = db.relationship(
        "GenreModel", secondary=TrackGenresModel, lazy="dynamic")
