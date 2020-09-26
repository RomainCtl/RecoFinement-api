from ..addons import db


class Tag(db.Model):
    """
    Tag Model for storing tag related details
    """
    tag_id = db.Column(db.Integer, primary_key=True,
                       autoincrement=True, index=True)
    name = db.Column(db.String(255), nullable=False)
