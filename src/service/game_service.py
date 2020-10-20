from flask import current_app
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator
from src.model import GameModel, MetaUserGameModel, GenreModel, ContentType, UserModel
from src.schemas import GameBase, GameObject, GenreBase, MetaUserGameBase


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
            game_data = GameObject.loads(games)

            return pagination_resp(
                message="Most popular track data sent",
                content=game_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_ordered_genre():
        genres = GenreModel.query.filter_by(
            content_type=ContentType.GAME).order_by(GenreModel.count.desc()).all()

        try:
            genres_data = GenreBase.loads(genres)

            resp = message(True, "Game genres data sent")
            resp["content"] = genres_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_meta(user_uuid, game_id):
        """ Get specific 'meta_user_track' data """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        try:
            if not (meta_user_game := MetaUserGameModel.query.filter_by(user_id=user.user_id, game_id=game_id).first()):
                meta_user_game = MetaUserGameModel(
                    game_id=game_id, user_id=user.user_id, review_see_count=0)

            # Increment meta see
            meta_user_game.review_see_count += 1
            db.session.add(meta_user_game)
            db.session.commit()

            meta_user_game_data = MetaUserGameBase.load(meta_user_game)

            resp = message(True, "Meta successfully sent")
            resp["content"] = meta_user_game_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def update_meta(user_uuid, game_id, data):
        """ Update 'hours' or/and 'purchase' or/and 'rating' """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (game := GameModel.query.filter_by(game_id=game_id).first()):
            return err_resp("Game not found!", 404)

        try:
            if not (meta_user_game := MetaUserGameModel.query.filter_by(user_id=user.user_id, game_id=game_id).first()):
                meta_user_game = MetaUserGameModel(
                    game_id=game_id, user_id=user.user_id, hours=0)

            if 'rating' in data:
                # Update average rating on object
                game.rating = game.rating or 0
                game.rating_count = game.rating_count or 0
                count = game.rating_count + \
                    (1 if meta_user_game.rating is None else 0)
                game.rating = (game.rating * game.rating_count - (
                    meta_user_game.rating if meta_user_game.rating is not None else 0) + data["rating"]) / count
                game.rating_count = count

                meta_user_game.rating = data["rating"]
            if 'hours' in data:
                meta_user_game.hours += data['hours']
            if 'purchase' in data:
                meta_user_game.purchase = data['purchase']

            db.session.add(meta_user_game)
            db.session.commit()

            resp = message(True, "Meta successfully updated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
