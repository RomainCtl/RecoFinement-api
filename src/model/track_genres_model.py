from src import db


class TrackGenresModel(db.Model):
    """
    TrackGenres Model for storing track genres
    """
    __tablename__ = "track_genres"

    track_id = db.Column(db.Integer, db.ForeignKey(
        "track.track_id"), primary_key=True)
    tag = db.Column(db.String(255), primary_key=True)
    frequency = db.Column(db.Integer)
