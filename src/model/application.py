from src import db


class Application(db.Model):
    """
    Application Model for storing application related details
    """
    app_id = db.Column(db.Integer, primary_key=True,
                       autoincrement=True, index=True)
    name = db.Column(db.String(255), unique=True, index=True)
    category = db.Column(db.String(255))
    rating = db.Column(db.Float)
    reviews = db.Column(db.Integer)
    size = db.Column(db.String(255))
    installs = db.Column(db.String(255))
    type = db.Column(db.String(45))
    price = db.Column(db.Float)
    content_rating = db.Column(db.String(255))
    genres = db.Column(db.String(255))
    last_updated = db.Column(db.String(255))
    current_version = db.Column(db.String(255))
    android_version = db.Column(db.String(255))
