def load_data(book_db_obj):
    """ Load book's data

    Parameters:
    - Book db object
    """
    from src.schemas.book import BookSchema

    book_schema = BookSchema()

    return book_schema.dump(book_db_obj)
