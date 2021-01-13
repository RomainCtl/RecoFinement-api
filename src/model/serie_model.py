from sqlalchemy.ext.hybrid import hybrid_property

from src import db


class SerieModel(db.Model):
    """
    Serie Model for storing serie related details
    """
    __tablename__ = "serie"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    imdbid = db.Column(db.String(255))
    title = db.Column(db.String(255), index=True)
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    writers = db.Column(db.Text)
    directors = db.Column(db.Text)
    actors = db.Column(db.Text)
    cover = db.Column(db.Text)
    plot_outline = db.Column(db.Text)

    episodes = db.relationship(
        "EpisodeModel", backref="serie",  lazy="dynamic")

    content = db.relationship(
        "ContentModel", backref=db.backref("serie", uselist=False))

    @hybrid_property
    def serie_id(self):
        return self.content_id
