def load_data(track_db_obj):
    """ Load track's data

    Parameters:
    - Track db object
    """
    from src.schemas.track import TrackSchema

    track_schema = TrackSchema()

    return track_schema.dump(track_db_obj)
