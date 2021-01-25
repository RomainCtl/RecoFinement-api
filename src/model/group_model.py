from src import db

InvitationModel = db.Table("invitations",
                           db.Column("user_id", db.Integer, db.ForeignKey(
                               "user.user_id", ondelete="CASCADE"), primary_key=True),
                           db.Column("group_id", db.Integer, db.ForeignKey(
                               "group.group_id", ondelete="CASCADE"), primary_key=True)
                           )


class RecommendedContentForGroupModel(db.Model):
    """
    RecommendedContent Model for storing recommended contents for a group
    """
    __tablename__ = "recommended_content_for_group"

    group_id = db.Column(db.Integer, db.ForeignKey(
        "group.group_id", ondelete="CASCADE"), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey(
        "content.content_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)
    engine_priority = db.Column(db.Integer)


class GroupModel(db.Model):
    """
    Group Model for storing group related details
    """
    __tablename__ = "group"

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"))

    invitations = db.relationship("UserModel", secondary=InvitationModel,
                                  lazy="dynamic", backref=db.backref("invitations", lazy="dynamic"))

    recommended_contents = db.relationship(
        "RecommendedContentForGroupModel", lazy="subquery")

#class GroupProfileModel(db.Model):
    """
    Group Model for storing group related details
    """
    """ __tablename__ = "group_profile"

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        "profile.profile_id", ondelete="CASCADE"))

    invitations = db.relationship("ProfileModel", secondary=InvitationModel,
                                  lazy="dynamic", backref=db.backref("invitations", lazy="dynamic"))

    recommended_contents = db.relationship(
        "RecommendedContentForGroupModel", lazy="subquery") """