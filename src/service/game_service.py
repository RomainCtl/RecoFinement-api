from flask import current_app, jsonify
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator
from src.model import GameModel, MetaUserGameModel
from src.schemas import GameBase


class GameService:
    @staticmethod
    def search_game_data(search_term, page):
        """ Search game data by title """
        games, total_pages = Paginator.get_from(
            GameModel.query.filter(GameModel.title.ilike(search_term+"%")).union(
                GameModel.query.filter(GameModel.title.ilike("%"+search_term+"%"))),
            page,
        )

        try:
            game_data = GameBase.loads(games)

            return pagination_resp(
                message="Game data sent",
                content=game_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_most_popular_games(page):
        games, total_pages = Paginator.get_from(
            GameModel.query.order_by(
                GameModel.recommendations.desc().nullslast()),
            page,
        )

        try:
            game_data = GameBase.loads(games)

            return pagination_resp(
                message="Most popular game data sent",
                content=game_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_game_data(id):
        """ Get game data by id """
        game = GameModel.query.filter(GameModel.game_id==id)
        try:
            game_data = GameBase.loads(game)

            return jsonify(
                message="Game data sent",
                content=game_data
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()