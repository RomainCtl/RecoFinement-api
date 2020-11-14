from src import db


class SimilarsBooksModel(db.Model):
    """
    SimilarsBooks Model for storing similars Book
    """
    __tablename__ = "similars_book"

    isbn0 = db.Column(db.String(13), db.ForeignKey(
        "book.isbn"), primary_key=True)
    isbn1 = db.Column(db.String(13), db.ForeignKey(
        "book.isbn"), primary_key=True)
    similarity = db.Column(db.Float)


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
    image_url_s = db.Column(db.Text)
    image_url_m = db.Column(db.Text)
    image_url_l = db.Column(db.Text)
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer, default=0)
    popularity_score = db.Column(db.Float, default=0)

    similars = db.relationship("BookModel", secondary=SimilarsBooksModel.__table__,
                               primaryjoin=isbn == SimilarsBooksModel.isbn0,
                               secondaryjoin=isbn == SimilarsBooksModel.isbn1,
                               lazy="subquery")
