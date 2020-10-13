from src import db


class SGameGenresModel(db.Model):
    """
    SGameGenres Model for storing game genres
    """
    __tablename__ = "s_game_genres"

    genre = db.Column(db.String(45), primary_key=True, index=True)
    count = db.Column(db.Integer)
