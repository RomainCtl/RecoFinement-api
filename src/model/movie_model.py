from src import db

MovieGenresModel = db.Table("movie_genres",
                            db.Column("movie_id", db.Integer, db.ForeignKey(
                                "movie.movie_id"), primary_key=True),
                            db.Column("genre_id", db.Integer, db.ForeignKey(
                                "genre.genre_id"), primary_key=True)
                            )


class SimilarsMoviesModel(db.Model):
    """
    SimilarsMovies Model for storing similars Movie
    """
    __tablename__ = "similars_movie"

    movie_id0 = db.Column(db.Integer, db.ForeignKey(
        "movie.movie_id"), primary_key=True)
    movie_id1 = db.Column(db.Integer, db.ForeignKey(
        "movie.movie_id"), primary_key=True)
    similarity = db.Column(db.Float)


class MovieModel(db.Model):
    """
    Movie Model for storing movie related details
    """
    __tablename__ = "movie"

    movie_id = db.Column(db.Integer, primary_key=True,
                         autoincrement=True, index=True)
    title = db.Column(db.String(255), index=True)
    language = db.Column(db.String(255))
    actors = db.Column(db.Text)
    year = db.Column(db.Integer)
    producers = db.Column(db.Text)
    director = db.Column(db.Text)
    writer = db.Column(db.Text)
    imdbid = db.Column(db.String(255))
    tmdbid = db.Column(db.String(255))
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer, default=0)
    cover = db.Column(db.Text)
    plot_outline = db.Column(db.Text)
    popularity_score = db.Column(db.Float, default=0)

    genres = db.relationship(
        "GenreModel", secondary=MovieGenresModel, lazy="dynamic")

    similars = db.relationship("MovieModel", secondary=SimilarsMoviesModel.__table__,
                               primaryjoin=movie_id == SimilarsMoviesModel.movie_id0,
                               secondaryjoin=movie_id == SimilarsMoviesModel.movie_id1,
                               lazy="subquery")
