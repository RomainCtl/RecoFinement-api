from sqlalchemy.ext.hybrid import hybrid_property

from src import db

EpisodeAdditionalGenresModel = db.Table("episode_additional_genres",
                              db.Column("imdbid", db.String(255), db.ForeignKey(
                                  "episode_additional.imdbid"), primary_key=True),
                              db.Column("genre_id", db.Integer, db.ForeignKey(
                                  "genre.genre_id"), primary_key=True)
                              )

class EpisodeModel(db.Model):
    """
    Episode Model for storing episode related details
    """
    __tablename__ = "episode"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    imdbid = db.Column(db.String(255))
    title = db.Column(db.String(512), index=True)
    year = db.Column(db.Integer)
    season_number = db.Column(db.Integer)
    episode_number = db.Column(db.Integer)
    serie_id = db.Column(db.Integer, db.ForeignKey("serie.content_id"))

    content = db.relationship(
        "ContentModel", backref=db.backref("episode", uselist=False))

    @hybrid_property
    def episode_id(self):
        return self.content_id

class EpisodeAdditionalModel(db.Model):
    """
    Episode Model for storing episode related details added by a user
    """
    __tablename__ = "episode_additional"

    imdbid = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(512), index=True)
    year = db.Column(db.Integer)
    season_number = db.Column(db.Integer)
    episode_number = db.Column(db.Integer)
    serie_id = db.Column(db.Integer, db.ForeignKey("serie_additional.imdbid"))

    genres = db.relationship(
        "GenreModel", secondary=EpisodeAdditionalGenresModel, lazy="dynamic")
