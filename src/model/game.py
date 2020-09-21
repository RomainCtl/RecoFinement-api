from sqlalchemy.dialects.postgresql import UUID
import uuid

from src import db

class Game(db.Model):
    """
    Game Model for storing game related details
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(255))
    icon_url = db.Column(db.String(255))
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer)
    price = db.Column(db.Float)
    in_app_purchases = db.Column(db.Float)
    description = db.Column(db.Text)
    developer = db.Column(db.String(255))
    languages = db.Column(db.String(255))
    size = db.Column(db.Integer)
    primary_genre = db.Column(db.String(45))
    genres = db.Column(db.String(255))
    original_release_date = db.Column(db.String(45))
