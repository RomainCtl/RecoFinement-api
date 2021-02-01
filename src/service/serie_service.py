from settings import REASON_CATEGORIES
from flask import current_app
from flask_jwt_extended import get_jwt_claims
from sqlalchemy import func, text, select, and_
from sqlalchemy.sql.expression import null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import SerieModel, EpisodeModel, GenreModel, ContentType, UserModel, ContentModel, RecommendedContentModel, RecommendedContentForGroupModel, MetaUserContentModel, BadRecommendationContentModel, SerieAdditionalModel, EpisodeAdditionalModel
from src.schemas import SerieBase, SerieItem, EpisodeBase, GenreBase, SerieExtra, MetaUserContentBase


class SerieService:
    @staticmethod
    def search_serie_data(search_term, page, connected_user_uuid):
        """ Search serie data by title """
        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)
        series, total_pages = Paginator.get_from(
            SerieModel.query.filter(SerieModel.title.ilike(search_term+"%")).union(
                SerieModel.query.filter(SerieModel.title.ilike("%"+search_term+"%"))),
            page,
        )

        try:
            serie_data = SerieBase.loads(series)

            return pagination_resp(
                message="Serie data sent",
                content=serie_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_popular_series(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        series, total_pages = Paginator.get_from(
            SerieModel.query.join(SerieModel.content, aliased=True).order_by(
                ContentModel.popularity_score.desc().nullslast(),
            ),
            page,
        )

        try:
            serie_data = SerieItem.loads(series)

            return pagination_resp(
                message="Most popular serie data sent",
                content=serie_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_recommended_series_for_user(page, connected_user_uuid, reco_engine):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        filters = [RecommendedContentModel.user_id == user.user_id]
        if reco_engine is not None:
            filters.append(RecommendedContentModel.engine == reco_engine)

        series, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentModel, SerieModel)
            .join(SerieModel.content)
            .join(RecommendedContentModel, RecommendedContentModel.content_id == ContentModel.content_id)
            .filter(
                and_(*filters)
            )
            .order_by(
                RecommendedContentModel.score.desc().nullslast(),
                ContentModel.popularity_score.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                serie = SerieExtra.load(row[1])
                serie["reco_engine"] = row[0].engine
                serie["reco_score"] = row[0].score
                return serie

            serie_data = list(map(c_load, series))

            return pagination_resp(
                message="Most popular serie data sent",
                content=serie_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_recommended_series_for_group(page, connected_user_uuid, reco_engine):
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

        series, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentForGroupModel, SerieModel)
            .join(SerieModel.content)
            .join(RecommendedContentForGroupModel, RecommendedContentForGroupModel.content_id == ContentModel.content_id)
            .filter(
                and_(*filters)
            )
            .order_by(
                RecommendedContentModel.score.desc().nullslast(),
                ContentModel.popularity_score.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                serie = SerieExtra.load(row[1])
                serie["reco_engine"] = row[0].engine
                serie["reco_score"] = row[0].score
                return serie

            serie_data = list(map(c_load, series))

            return pagination_resp(
                message="Most popular serie data sent",
                content=serie_data,
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
            content_type=ContentType.SERIE).order_by(GenreModel.count.desc()).all()

        try:
            genres_data = GenreBase.loads(genres)

            resp = message(True, "Serie genres data sent")
            resp["content"] = genres_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_episodes(content_id):
        if not (episodes := EpisodeModel.query.filter_by(serie_id=content_id).order_by(EpisodeModel.season_number, EpisodeModel.episode_number).all()):
            return err_resp("Serie not found!", 404)

        try:
            episodes_data = EpisodeBase.loads(episodes)

            resp = message(True, "Series episodes data sent")
            resp["content"] = episodes_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def add_bad_recommendation(user_uuid, content_id, data):
        """ Add bad user recommendation """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (serie := SerieModel.query.filter_by(content_id=content_id).first()):
            return err_resp("Serie not found!", 404)

        try:
            for type, value in data.items():
                if type in REASON_CATEGORIES['serie']:
                    for r in value:

                        new_bad_reco = BadRecommendationContentModel(
                            user_id=user.user_id,
                            content_id=serie.content_id,
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
    def add_additional_serie(user_uuid, data):
        """ Add additional serie"""
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "add_content" not in permissions:
            return err_resp("Permission missing", 403)

        try:

            new_additional_serie = SerieAdditionalModel(
                title=data['title'],
            )

            if 'imdbid' in data:
                new_additional_serie.imdbid = data['imdbid']
            if 'start_year' in data:
                new_additional_serie.start_year = data['start_year']
            if 'end_year' in data:
                new_additional_serie.end_year = data['end_year']
            if 'writers' in data:
                new_additional_serie.writers = data['writers']
            if 'directors' in data:
                new_additional_serie.directors = data['directors']
            if 'actors' in data:
                new_additional_serie.actors = data['actors']
            if 'cover' in data:
                new_additional_serie.cover = data['cover']

            for genre_id in data["genres"]:
                if (ge := GenreModel.query.filter_by(genre_id=genre_id).first()):
                    new_additional_serie.genres.append(ge)
                else:
                    return err_resp("Genre %s not found!" % genre_id, 404)

            db.session.add(new_additional_serie)
            db.session.flush()

            if "episodes" in data:
                for episode in data["episodes"]:
                    new_additional_episode = EpisodeAdditionalModel(
                        title=data['title'],
                        serie_id=new_additional_serie.serie_id
                    )

                    if 'imdbid' in data:
                        new_additional_serie.imdbid = data['imdbid']
                    if 'year' in data:
                        new_additional_serie.year = data['year']
                    if 'season_number' in data:
                        new_additional_serie.season_number = data['season_number']
                    if 'episode_number' in data:
                        new_additional_serie.episode_number = data['episode_number']

                    for genre_id in data["genres"]:
                        if (ge := GenreModel.query.filter_by(genre_id=genre_id).first()):
                            new_additional_episode.genres.append(ge)
                        else:
                            return err_resp("Genre %s not found!" % genre_id, 404)

                    db.session.add(new_additional_episode)

            db.session.commit()

            resp = message(True, "Serie have been added to validation.")
            return resp, 201

        except Exception as error:
            import traceback
            traceback.print_exc()
            current_app.logger.error(error)
            return internal_err_resp()
