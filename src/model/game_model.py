from sqlalchemy.ext.hybrid import hybrid_property

from src import db

GameAdditionalGenresModel = db.Table("game_additional_genres",
                              db.Column("game_id", db.Integer, db.ForeignKey(
                                  "game_additional.game_id"), primary_key=True),
                              db.Column("genre_id", db.Integer, db.ForeignKey(
                                  "genre.genre_id"), primary_key=True)
                              )

class GameModel(db.Model):
    """
    Game Model for storing game related details
    """
    __tablename__ = "game"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    steamid = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(255), index=True)
    short_description = db.Column(db.Text)
    header_image = db.Column(db.String(255))
    website = db.Column(db.String(255))
    developers = db.Column(db.String(255))
    publishers = db.Column(db.String(255))
    price = db.Column(db.String(255))
    recommendations = db.Column(db.Integer)
    release_date = db.Column(db.String(255))

    content = db.relationship(
        "ContentModel", backref=db.backref("game", uselist=False))

    @hybrid_property
    def game_id(self):
        return self.content_id


class GameAdditionalModel(db.Model):
    """
    Game Model for storing game related details added by a user
    """
    __tablename__ = "game_additional"

    game_id = db.Column(db.Integer, primary_key=True, index=True)
    steamid = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(255), index=True)
    short_description = db.Column(db.Text)
    header_image = db.Column(db.String(255))
    website = db.Column(db.String(255))
    developers = db.Column(db.String(255))
    publishers = db.Column(db.String(255))
    price = db.Column(db.String(255))
    release_date = db.Column(db.String(255))

    genres = db.relationship(
        "GenreModel", secondary=GameAdditionalGenresModel, lazy="dynamic")