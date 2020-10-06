from src import db


class BookModel(db.Model):
    """
    Book Model for storing book related details
    """
    __tablename__ = "book"

    isbn = db.Column(db.String(13), primary_key=True,
                     nullable=False, index=True)
    title = db.Column(db.String(255), index=True)
    author = db.Column(db.String(255), index=True)
    year_of_publication = db.Column(db.Integer)
    publisher = db.Column(db.String(255))
    image_url_s = db.Column(db.String(255))
    image_url_m = db.Column(db.String(255))
    image_url_l = db.Column(db.String(255))
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer, default=0)
