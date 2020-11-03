from src import db

class ExternalModel(db.Model):
    """
    External service Model for storing user service related details
    """
    __tablename__ = "external_service"
    __table_args__ = (
        db.UniqueConstraint('user_id', 'service_name', name='unique_userID_serviceName'),
    )
    service_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), nullable=False)
    service_name = db.Column(db.String(45), nullable=False)
    access_token = db.Column(db.Text, default=None)
    refresh_token = db.Column(db.Text, default=None)