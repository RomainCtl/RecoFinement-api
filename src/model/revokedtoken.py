from src import db

class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(255))

    @staticmethod
    def is_revoked(jti) -> bool:
        return bool( RevokedToken.query.filter_by(jti=jti).first() )
