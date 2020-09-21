from ..addons import db

class Tag(db.model):
    """
    Tag Model for storing tag related details
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
