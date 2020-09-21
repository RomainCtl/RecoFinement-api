from sqlalchemy.dialects.postgresql import UUID
import uuid

from src import db

class Genre(db.Model):
    """
    Genre Model for storing genre related details
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
