from sqlalchemy.ext.hybrid import hybrid_property

from src import db

BookAdditionalGenresModel = db.Table("book_additional_genres",
                              db.Column("isbn", db.String(13), db.ForeignKey(
                                  "book_additional.isbn"), primary_key=True),
                              db.Column("genre_id", db.Integer, db.ForeignKey(
                                  "genre.genre_id"), primary_key=True)
                              )

class BookModel(db.Model):
    """
    Book Model for storing book related details
    """
    __tablename__ = "book"

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('content.content_id', ondelete="CASCADE"),
        primary_key=True, index=True)
    isbn = db.Column(db.String(13), unique=True,
                     nullable=False, index=True)
    title = db.Column(db.String(255), index=True)
    author = db.Column(db.String(255), index=True)
    year_of_publication = db.Column(db.Integer)
    publisher = db.Column(db.String(255))
    image_url_s = db.Column(db.Text)
    image_url_m = db.Column(db.Text)
    image_url_l = db.Column(db.Text)

    content = db.relationship(
        "ContentModel", backref=db.backref("book", uselist=False))

    @hybrid_property
    def book_id(self):
        return self.content_id

class BookAdditionalModel(db.Model):
    """
    Book Model for storing book related details added by a user
    """
    __tablename__ = "book_additional"

    isbn = db.Column(db.String(13), unique=True, primary_key=True
                     nullable=False, index=True)
    title = db.Column(db.String(255), index=True)
    author = db.Column(db.String(255), index=True)
    year_of_publication = db.Column(db.Integer)
    publisher = db.Column(db.String(255))
    image_url_s = db.Column(db.Text)
    image_url_m = db.Column(db.Text)
    image_url_l = db.Column(db.Text)

    genres = db.relationship(
        "GenreModel", secondary=BookAdditionalGenresModel, lazy="dynamic")
