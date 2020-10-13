from src import db


class STrackGenresModel(db.Model):
    """
    STrackGenres Model for storing track genres
    """
    __tablename__ = "s_track_genres"

    genre = db.Column(db.String(45), primary_key=True, index=True)
    count = db.Column(db.Integer)
