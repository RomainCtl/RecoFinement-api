from src import db


class Game(db.Model):
    """
    Game Model for storing game related details
    """
    game_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, index=True)
    steamid = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(255), index=True)
    short_description = db.Column(db.Text)
    header_image = db.Column(db.String(255))
    website = db.Column(db.String(255))
    developers = db.Column(db.String(255))
    publishers = db.Column(db.String(255))
    price = db.Column(db.String(255))
    genres = db.Column(db.String(255))
    recommendations = db.Column(db.String(255))
    release_date = db.Column(db.String(255))
