from settings import REASON_CATEGORIES
from flask import current_app
from flask_jwt_extended import get_jwt_claims
from sqlalchemy import func, text, select
from sqlalchemy.sql.expression import null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import GameModel, MetaUserGameModel, GenreModel, ContentType, UserModel, RecommendedGameModel, RecommendedGameForGroupModel, BadRecommendationGameModel
from src.schemas import GameBase, GameObject, GenreBase, MetaUserGameBase, GameExtra


class GameService:
    @staticmethod
    def search_game_data(search_term, page, connected_user_uuid):
        """ Search game data by name """
        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)
        games, total_pages = Paginator.get_from(
            GameModel.query.filter(GameModel.name.ilike(search_term+"%")).union(
                GameModel.query.filter(GameModel.name.ilike("%"+search_term+"%"))),
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
    def get_recommended_games(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "view_recommendation" not in permissions:
            return err_resp("Permission missing", 403)

        # Query for recommendation from user
        for_user_query = db.session.query(RecommendedGameModel, GameModel)\
            .select_from(RecommendedGameModel)\
            .outerjoin(GameModel, GameModel.game_id == RecommendedGameModel.game_id)\
            .filter(RecommendedGameModel.user_id == user.user_id)

        # Query for recommendation from group
        groups_ids = [
            *list(map(lambda x: x.group_id, user.groups)),
            *list(map(lambda x: x.group_id, user.owned_groups))
        ]

        for_group_query = db.session.query(RecommendedGameForGroupModel, GameModel)\
            .select_from(RecommendedGameForGroupModel)\
            .outerjoin(GameModel, GameModel.game_id == RecommendedGameForGroupModel.game_id)\
            .filter(RecommendedGameForGroupModel.group_id.in_(groups_ids))

        # NOTE we do not have any rating for game (cold start), so we use 'recommendations' field instead of 'popularity_score' that is computed by 'reco_engine' service
        popularity_query = db.session.query(
            func.cast(null(), db.Integer),
            func.cast(null(), db.Integer),
            func.cast(null(), db.Float),
            null(),
            func.cast(null(), db.Integer),
            GameModel
        ).order_by(
            GameModel.recommendations.desc().nullslast(),
        ).limit(200).subquery()

        games, total_pages = Paginator.get_from(
            for_user_query
            .union(for_group_query)
            .union(select([popularity_query]))
            .order_by(
                RecommendedGameModel.engine_priority.desc().nullslast(),
                RecommendedGameModel.score.desc(),
                GameModel.recommendations.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                if row[0] is None:
                    game = GameExtra.load(row[1])
                else:
                    game = GameExtra.load(row[1])
                    game["reco_engine"] = row[0].engine
                    game["reco_score"] = row[0].score
                return game

            game_data = list(map(c_load, games))

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
    def get_ordered_genre(connected_user_uuid):
        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)
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

        if not (GameModel.query.filter_by(game_id=game_id).first()):
            return err_resp("Game not found!", 404)

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
        """ Update 'additional_hours' or/and 'purchase' or/and 'rating' """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "indicate_interest" not in permissions:
            return err_resp("Permission missing", 403)

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
            if 'additional_hours' in data:
                meta_user_game.hours += data['additional_hours']
            if 'purchase' in data:
                meta_user_game.purchase = data['purchase']

            db.session.add(meta_user_game)
            db.session.commit()

            resp = message(True, "Meta successfully updated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def add_bad_recommendation(user_uuid, game_id, data):
        """ Add bad user recommendation """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "indicate_interest" not in permissions:
            return err_resp("Permission missing", 403)

        if not (game := GameModel.query.filter_by(game_id=game_id).first()):
            return err_resp("Game not found!", 404)

        try:
            for rc in data['reason_categorie']:
                if rc in REASON_CATEGORIES['game']:
                    for r in data['reason']:

                        new_bad_reco = BadRecommendationGameModel(
                            user_id=user.id,
                            game_id=game.game_id,
                            reason_categorie=rc,
                            reason=r
                        )

                        db.session.add(new_bad_reco)
                        db.session.flush()
            db.session.commit()

            resp = message(True, "Bad recommendation has been registered.")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
