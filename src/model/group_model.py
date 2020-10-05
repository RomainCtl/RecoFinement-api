from src import db

InvitationModel = db.Table("invitations",
                           db.Column("user_id", db.Integer, db.ForeignKey(
                               "user.user_id"), primary_key=True),
                           db.Column("group_id", db.Integer, db.ForeignKey(
                               "group.group_id"), primary_key=True)
                           )


class GroupModel(db.Model):
    """
    Group Model for storing group related details
    """
    __tablename__ = "group"

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    invitations = db.relationship("UserModel", secondary=InvitationModel,
                                  lazy="dynamic", backref=db.backref("invitations", lazy="dynamic"))
