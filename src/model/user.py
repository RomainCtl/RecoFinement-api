from sqlalchemy.dialects.postgresql import UUID
import uuid

from src import db, bcrypt

class User(db.Model):
    """
    User Model for storing user related details
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(45), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
