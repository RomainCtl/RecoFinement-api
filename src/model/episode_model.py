from src import db


class EpisodeModel(db.Model):
    """
    Episode Model for storing episode related details
    """
    __tablename__ = "episode"

    episode_id = db.Column(db.Integer, primary_key=True,
                           autoincrement=True, index=True)
    imdbid = db.Column(db.String(255))
    title = db.Column(db.String(512), index=True)
    year = db.Column(db.Integer)
    genres = db.Column(db.Text)
    season_number = db.Column(db.Integer)
    episode_number = db.Column(db.Integer)
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer, default=0)
    serie_id = db.Column(db.Integer, db.ForeignKey("serie.serie_id"))
