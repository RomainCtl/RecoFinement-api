def load_data(game_db_obj):
    """ Load game's data

    Parameters:
    - Game db object
    """
    from src.schemas.game import GameSchema

    game_schema = GameSchema()

    return game_schema.dump(game_db_obj)
