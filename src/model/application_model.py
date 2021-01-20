from sqlalchemy.ext.hybrid import hybrid_property

from src import db

ApplicationAdditionalGenresModel = db.Table("application_additional_genres",
                              db.Column("app_id", db.Integer, db.ForeignKey(
                                  "application_additional.app_id"), primary_key=True),
                              db.Column("genre_id", db.Integer, db.ForeignKey(
                                  "genre.genre_id"), primary_key=True)
                              )

class ApplicationModel(db.Model):
    """
    Application Model for storing application related details
    """
    __tablename__ = "application"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True, index=True)
    size = db.Column(db.String(255))
    installs = db.Column(db.String(255))
    type = db.Column(db.String(45))
    price = db.Column(db.String(45))
    content_rating = db.Column(db.String(255))
    last_updated = db.Column(db.String(255))
    current_version = db.Column(db.String(255))
    android_version = db.Column(db.String(255))
    cover = db.Column(db.Text)

    content = db.relationship(
        "ContentModel", backref=db.backref("application", uselist=False))

    @hybrid_property
    def app_id(self):
        return self.content_id

    @hybrid_property
    def categorie(self):
        return self.content.genres[0] if self.content.genres else None

class ApplicationAdditionalModel(db.Model):
    """
    Application Model for storing application related details added by a user
    """
    __tablename__ = "application_additional"

    app_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True, index=True)
    size = db.Column(db.String(255))
    installs = db.Column(db.String(255))
    type = db.Column(db.String(45))
    price = db.Column(db.String(45))
    content_rating = db.Column(db.String(255))
    last_updated = db.Column(db.String(255))
    current_version = db.Column(db.String(255))
    android_version = db.Column(db.String(255))
    cover = db.Column(db.Text)

    genres = db.relationship("GenreModel", secondary=ApplicationAdditionalGenresModel, lazy="dynamic")