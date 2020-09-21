from sqlalchemy.dialects.postgresql import UUID
import uuid

from src import db

class Application(db.Model):
    """
    Application Model for storing application related details
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    app_name = db.Column(db.String(255), unique=True, index=True)
    category = db.Column(db.String(255))
    rating = db.Column(db.Float)
    reviews = db.Column(db.Integer)
    installs = db.Column(db.String(255))
    size = db.Column(db.String(255))
    price = db.Column(db.Float)
    content_rating = db.Column(db.String(255))
    last_updated = db.Column(db.String(255))
    minimum_version = db.Column(db.String(255))
    latest_version = db.Column(db.String(255))