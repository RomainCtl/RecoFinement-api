from sqlalchemy.ext.hybrid import hybrid_property

from src import db


class MovieModel(db.Model):
    """
    Movie Model for storing movie related details
    """
    __tablename__ = "movie"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    title = db.Column(db.String(255), index=True)
    language = db.Column(db.String(255))
    actors = db.Column(db.Text)
    year = db.Column(db.String(255))
    producers = db.Column(db.Text)
    director = db.Column(db.Text)
    writer = db.Column(db.Text)
    imdbid = db.Column(db.String(255))
    tmdbid = db.Column(db.String(255))
    cover = db.Column(db.Text)
    plot_outline = db.Column(db.Text)

    content = db.relationship(
        "ContentModel", backref=db.backref("movie", uselist=False))

    @hybrid_property
    def movie_id(self):
        return self.content_id
