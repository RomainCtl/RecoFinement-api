def load_data(user_db_obj):
    """ Load user's data

    Parameters:
    - User db object
    """
    from src.schemas import UserObject

    user_schema = UserObject()

    return user_schema.dump(user_db_obj)
