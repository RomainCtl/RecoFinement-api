from src import db

SerieGenresModel = db.Table("serie_genres",
                            db.Column("serie_id", db.Integer, db.ForeignKey(
                                "serie.serie_id"), primary_key=True),
                            db.Column("genre_id", db.Integer, db.ForeignKey(
                                "genre.genre_id"), primary_key=True)
                            )


class SimilarsSeriesModel(db.Model):
    """
    SimilarsSeries Model for storing similars Serie
    """
    __tablename__ = "similars_serie"

    serie_id0 = db.Column(db.Integer, db.ForeignKey(
        "serie.serie_id"), primary_key=True)
    serie_id1 = db.Column(db.Integer, db.ForeignKey(
        "serie.serie_id"), primary_key=True)
    similarity = db.Column(db.Float)


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
    writers = db.Column(db.Text)
    directors = db.Column(db.Text)
    actors = db.Column(db.Text)
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer, default=0)
    cover = db.Column(db.Text)
    plot_outline = db.Column(db.Text)
    popularity_score = db.Column(db.Float, default=0)

    genres = db.relationship(
        "GenreModel", secondary=SerieGenresModel, lazy="dynamic")

    episodes = db.relationship(
        "EpisodeModel", backref="serie",  lazy="dynamic")

    similars = db.relationship("SerieModel", secondary=SimilarsSeriesModel.__table__,
                               primaryjoin=serie_id == SimilarsSeriesModel.serie_id0,
                               secondaryjoin=serie_id == SimilarsSeriesModel.serie_id1,
                               lazy="subquery")
