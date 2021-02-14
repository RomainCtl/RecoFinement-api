from src import db
from .content_model import ContentType


class EngineModel(db.Model):
    """
    Engine Model for storing content related details
    """
    __tablename__ = "engine"

    engine = db.Column(db.String, primary_key=True)
    content_type = db.Column(db.Enum(ContentType), primary_key=True)
    last_launch_date = db.Column(db.DateTime)
