from src import db


class RevokedTokenModel(db.Model):
    __tablename__ = "revoked_token"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(255))

    @staticmethod
    def is_revoked(jti) -> bool:
        return bool(RevokedTokenModel.query.filter_by(jti=jti).first())
