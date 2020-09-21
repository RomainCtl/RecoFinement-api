from flask import current_app

from src.utils import err_resp, message, internal_err_resp
from src.model import Game


class GameService:
    @staticmethod
    def get_game_data(uid):
        """ Get game data by uid """
        if not (game := Game.query.filter_by(uid=uid).first()):
            return err_resp("Game not found!", "game_404", 404)

        from .utils import load_data

        try:
            game_data = load_data(game)

            resp = message(True, "Game data sent")
            resp["game"] = game_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
