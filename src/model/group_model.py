from src import db


class GroupModel(db.Model):
    """
    Group Model for storing group related details
    """
    __tablename__ = "group"

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
