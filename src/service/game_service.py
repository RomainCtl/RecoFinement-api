from flask import current_app
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
            db.session.query(GameModel, func.count(
                MetaUserGameModel.user_id).label("count")).outerjoin(MetaUserGameModel).group_by(GameModel.game_id).order_by(text("count DESC")),
            page,
        )

        try:
            games = map(lambda t: t[0], games)
            game_data = GameBase.loads(games)

            return pagination_resp(
                message="Most popular track data sent",
                content=game_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
