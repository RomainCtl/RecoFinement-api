from sqlalchemy.ext.hybrid import hybrid_property

from src import db


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
