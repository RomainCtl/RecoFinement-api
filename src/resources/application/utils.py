def load_data(application_db_obj):
    """ Load application's data

    Parameters:
    - Application db object
    """
    from src.schemas import ApplicationSchema

    application_schema = ApplicationSchema()

    return application_schema.dump(application_db_obj)
