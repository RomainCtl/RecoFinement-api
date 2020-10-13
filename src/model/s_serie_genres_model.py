from src import db


class SSerieGenresModel(db.Model):
    """
    SSerieGenres Model for storing serie genres
    """
    __tablename__ = "s_serie_genres"

    genre = db.Column(db.String(45), primary_key=True, index=True)
    count = db.Column(db.Integer)
