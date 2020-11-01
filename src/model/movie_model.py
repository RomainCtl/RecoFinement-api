from src import db

MovieGenresModel = db.Table("movie_genres",
                            db.Column("movie_id", db.Integer, db.ForeignKey(
                                "movie.movie_id"), primary_key=True),
                            db.Column("genre_id", db.Integer, db.ForeignKey(
                                "genre.genre_id"), primary_key=True)
                            )


class MovieModel(db.Model):
    """
    Movie Model for storing movie related details
    """
    __tablename__ = "movie"

    movie_id = db.Column(db.Integer, primary_key=True,
                         autoincrement=True, index=True)
    title = db.Column(db.String(255), index=True)
    language = db.Column(db.String(255))
    actors = db.Column(db.String(255))
    year = db.Column(db.String(255))
    producers = db.Column(db.String(255))
    director = db.Column(db.String(255))
    writer = db.Column(db.String(255))
    imdbid = db.Column(db.String(255))
    tmdbid = db.Column(db.String(255))
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer, default=0)
    cover = db.Column(db.Text)
    popularity_score = db.Column(db.Float, default=0)

    genres = db.relationship(
        "GenreModel", secondary=MovieGenresModel, lazy="dynamic")
