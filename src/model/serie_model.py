from src import db


class SerieModel(db.Model):
    """
    Serie Model for storing serie related details
    """
    __tablename__ = "serie"

    serie_id = db.Column(db.Integer, primary_key=True,
                         autoincrement=True, index=True)
    imdbid = db.Column(db.String(255))
    title = db.Column(db.String(255), index=True)
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    genres = db.Column(db.Text)
    writers = db.Column(db.Text)
    directors = db.Column(db.Text)
    actors = db.Column(db.Text)

    episodes = db.relationship(
        "EpisodeModel", backref="serie",  lazy="dynamic")
