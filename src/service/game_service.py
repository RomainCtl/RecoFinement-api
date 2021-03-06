from settings import REASON_CATEGORIES
from flask import current_app
from flask_jwt_extended import get_jwt_claims
from sqlalchemy import func, text, select, and_
from sqlalchemy.sql.expression import null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import GameModel, GenreModel, ContentType, UserModel, ContentModel, RecommendedContentModel, RecommendedContentForGroupModel, MetaUserContentModel, BadRecommendationContentModel, GameAdditionalModel
from src.schemas import GameBase, GameObject, GenreBase, GameExtra, MetaUserContentBase, GameAdditionalBase


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
    def get_popular_games(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # NOTE we do not have any rating for game (cold start), so we use 'recommendations' field instead of 'popularity_score' that is computed by 'reco_engine' service
        games, total_pages = Paginator.get_from(
            GameModel.query.join(GameModel.content, aliased=True).order_by(
                GameModel.recommendations.desc().nullslast(),
            ),
            page,
        )

        try:
            game_data = GameObject.loads(games)

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
    def get_recommended_games_for_user(page, connected_user_uuid, reco_engine):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        filters = [RecommendedContentModel.user_id == user.user_id]
        if reco_engine is not None:
            filters.append(RecommendedContentModel.engine == reco_engine)

        games, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentModel, GameModel)
            .join(GameModel.content)
            .join(RecommendedContentModel, RecommendedContentModel.content_id == ContentModel.content_id)
            .filter(
                and_(*filters)
            )
            .order_by(
                RecommendedContentModel.score.desc().nullslast(),
                GameModel.recommendations.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                app = GameExtra.load(row[1])
                app["reco_engine"] = row[0].engine
                app["reco_score"] = row[0].score
                return app

            game_data = list(map(c_load, games))

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
    def get_recommended_games_for_group(page, connected_user_uuid, reco_engine):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Query for recommendation from group
        groups_ids = [
            *list(map(lambda x: x.group_id, user.groups)),
            *list(map(lambda x: x.group_id, user.owned_groups))
        ]

        filters = [RecommendedContentForGroupModel.group_id.in_(groups_ids)]
        if reco_engine is not None:
            filters.append(RecommendedContentModel.engine == reco_engine)

        games, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentForGroupModel, GameModel)
            .join(GameModel.content)
            .join(RecommendedContentForGroupModel, RecommendedContentForGroupModel.content_id == ContentModel.content_id)
            .filter(
                and_(*filters)
            )
            .order_by(
                RecommendedContentModel.score.desc().nullslast(),
                GameModel.recommendations.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                app = GameExtra.load(row[1])
                app["reco_engine"] = row[0].engine
                app["reco_score"] = row[0].score
                return app

            game_data = list(map(c_load, games))

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
    def add_bad_recommendation(user_uuid, content_id, data):
        """ Add bad user recommendation """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (game := GameModel.query.filter_by(content_id=content_id).first()):
            return err_resp("Game not found!", 404)

        try:
            for type, value in data.items():
                if type in REASON_CATEGORIES['game']:
                    for r in value:

                        new_bad_reco = BadRecommendationContentModel(
                            user_id=user.user_id,
                            content_id=game.content_id,
                            reason_categorie=type,
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

    @staticmethod
    def add_additional_game(user_uuid, data):
        """ Add additional game"""
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "add_content" not in permissions:
            return err_resp("Permission missing", 403)

        try:

            new_additional_game = GameAdditionalModel(
                name=data['name'],
                steamid=data['steamid'],
            )

            if 'short_description' in data:
                new_additional_game.short_description = data['short_description']
            if 'header_image' in data:
                new_additional_game.header_image = data['header_image']
            if 'website' in data:
                new_additional_game.website = data['website']
            if 'developers' in data:
                new_additional_game.developers = data['developers']
            if 'publishers' in data:
                new_additional_game.publishers = data['publishers']
            if 'price' in data:
                new_additional_game.price = data['price']
            if 'release_date' in data:
                new_additional_game.release_date = data['release_date']

            for genre_id in data["genres"]:
                if (ge := GenreModel.query.filter_by(genre_id=genre_id).first()):
                    new_additional_game.genres.append(ge)
                else:
                    return err_resp("Genre %s not found!" % genre_id, 404)

            db.session.add(new_additional_game)
            db.session.commit()

            resp = message(True, "Game have been added to validation.")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_additional_game(connected_user_uuid, page):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "add_content" not in permissions:
            return err_resp("Permission missing", 403)

        games, total_pages = Paginator.get_from(
            GameAdditionalModel.query,
            page,
        )

        try:
            games_data = GameAdditionalBase.loads(games)

            return pagination_resp(
                message="Additional game data sent",
                content=games_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def validate_additional_game(connected_user_uuid, game_id):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "validate_added_content" not in permissions:
            return err_resp("Permission missing", 403)

        if not (game := GameAdditionalModel.query.filter_by(game_id=game_id).first()):
            return err_resp("Additional game not found!", 404)

        try:
            content = ContentModel(rating=None, genres=game.genres)
            db.session.add(content)
            db.session.flush()

            new_game = GameModel(
                steamid=game.steamid,
                name=game.name,
                short_description=game.short_description,
                header_image=game.header_image,
                website=game.website,
                developers=game.developers,
                publishers=game.publishers,
                price=game.price,
                release_date=game.release_date,
                content=content
            )
            db.session.add(new_game)
            db.session.delete(game)

            db.session.commit()

            resp = message(
                True, "Additional game data successfully validated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def decline_additional_game(connected_user_uuid, game_id):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "delete_content" not in permissions:
            return err_resp("Permission missing", 403)

        if not (game := GameAdditionalModel.query.filter_by(game_id=game_id).first()):
            return err_resp("Additional game not found!", 404)

        try:
            db.session.delete(game)
            db.session.commit()

            resp = message(True, "Additional game successfully deleted")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
